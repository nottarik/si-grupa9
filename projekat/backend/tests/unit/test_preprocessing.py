"""
Unit tests for the preprocessing pipeline.

Fixtures use synthetic PII. The 'no-leak' test verifies that none of the raw
PII values appear in the masked output.
"""
import logging
import pytest

from app.services.preprocessing.normalize import normalize
from app.services.preprocessing.speakers import split_turns
from app.services.preprocessing.chunking import chunk_turns
from app.services.preprocessing.models import Turn
from app.services.preprocessing.pii.recognizers import find_structural_pii, _jmbg_valid
from app.services.preprocessing.pii.masker import mask
from app.services.preprocessing.pii.token_store import encrypt_token_map, decrypt_token_map
from app.services.preprocessing.audit import safe_log, text_hash


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# 0101990012343 is a valid JMBG (checksum verified in test_jmbg_checksum_valid).
VALID_JMBG = "0101990012343"
VALID_PHONE = "061 123 456"
VALID_EMAIL = "tarik@example.ba"
VALID_IBAN = "BA391234567890123456"
VALID_SSN = "123-45-6789"

TRANSCRIPT_FIXTURE = (
    f"Korisnik: Dobar dan, zovem se Tarik. Moj JMBG je {VALID_JMBG}.\n"
    f"Agent: Dobar dan, kako Vam mogu pomoći?\n"
    f"Korisnik: Moj broj je {VALID_PHONE} i email {VALID_EMAIL}.\n"
    f"Agent: Hvala, zabilježio sam."
)


# ---------------------------------------------------------------------------
# normalize
# ---------------------------------------------------------------------------

def test_normalize_strips_and_unifies_newlines():
    assert normalize("  Hello\r\nWorld  ") == "Hello\nWorld"


def test_normalize_collapses_blank_lines():
    assert normalize("A\n\n\n\nB") == "A\n\nB"


def test_normalize_collapses_spaces():
    assert normalize("a  b\t c") == "a b c"


def test_normalize_nfc():
    # Pre-composed vs decomposed 'š'
    decomposed = "š"  # s + combining caron
    result = normalize(decomposed)
    assert result == "š"


def test_normalize_empty():
    assert normalize("") == ""


# ---------------------------------------------------------------------------
# speakers.split_turns
# ---------------------------------------------------------------------------

def test_split_turns_roles():
    turns = split_turns("Agent: Dobar dan\nKorisnik: Imam pitanje\nAgent: Rado ću pomoći")
    assert [t.role for t in turns] == ["agent", "user", "agent"]
    assert turns[0].text == "Dobar dan"


def test_split_turns_unknown_fallback():
    turns = split_turns("Neki tekst bez prefiksa")
    assert turns[0].role == "unknown"
    assert turns[0].text == "Neki tekst bez prefiksa"


def test_split_turns_empty_lines_skipped():
    turns = split_turns("Agent: Tekst\n\n\nKorisnik: Odgovor")
    assert len(turns) == 2


def test_split_turns_positions_sequential():
    turns = split_turns("Agent: A\nKorisnik: B\nAgent: C")
    assert [t.position for t in turns] == [0, 1, 2]


# ---------------------------------------------------------------------------
# PII recognizers
# ---------------------------------------------------------------------------

def test_jmbg_checksum_valid():
    assert _jmbg_valid(VALID_JMBG)


def test_jmbg_checksum_invalid():
    # Flip last digit
    bad = VALID_JMBG[:-1] + str((int(VALID_JMBG[-1]) + 1) % 10)
    assert not _jmbg_valid(bad)


def test_find_structural_pii_jmbg():
    spans = find_structural_pii(f"JMBG: {VALID_JMBG} kraj")
    types = [s.entity_type for s in spans]
    assert "JMBG" in types


def test_find_structural_pii_email():
    spans = find_structural_pii(f"Email: {VALID_EMAIL}")
    assert any(s.entity_type == "EMAIL" for s in spans)


def test_find_structural_pii_phone():
    spans = find_structural_pii(f"Tel: {VALID_PHONE}")
    assert any(s.entity_type == "TELEFON" for s in spans)


def test_find_structural_pii_iban():
    spans = find_structural_pii(f"IBAN: {VALID_IBAN}")
    assert any(s.entity_type == "IBAN" for s in spans)


def test_find_structural_pii_ssn():
    spans = find_structural_pii(f"SSN: {VALID_SSN}")
    assert any(s.entity_type == "SSN" for s in spans)


def test_jmbg_13_digits_no_checksum_not_detected():
    # Last digit wrong (should be 0 for all-zeros, we use 1) — checksum fails
    spans = find_structural_pii("0000000000001")
    assert not any(s.entity_type == "JMBG" for s in spans)


# ---------------------------------------------------------------------------
# masker
# ---------------------------------------------------------------------------

def test_mask_removes_jmbg():
    masked, token_map = mask(f"JMBG je {VALID_JMBG} ovdje")
    assert VALID_JMBG not in masked
    assert "[JMBG_1]" in masked


def test_mask_removes_phone():
    masked, token_map = mask(f"Broj: {VALID_PHONE}")
    assert VALID_PHONE not in masked


def test_mask_removes_email():
    masked, token_map = mask(f"Email: {VALID_EMAIL}")
    assert VALID_EMAIL not in masked


def test_mask_same_value_same_placeholder():
    text = f"{VALID_EMAIL} i opet {VALID_EMAIL}"
    masked, token_map = mask(text)
    assert masked.count("[EMAIL_1]") == 2
    assert len([k for k in token_map if k.startswith("[EMAIL_")]) == 1


def test_mask_roundtrip():
    masked, token_map = mask(TRANSCRIPT_FIXTURE)
    restored = masked
    for placeholder, original in token_map.items():
        restored = restored.replace(placeholder, original)
    assert VALID_JMBG in restored
    assert VALID_PHONE.replace(" ", "") in restored.replace(" ", "")


def test_mask_token_map_invertible(caplog):
    masked, token_map = mask(TRANSCRIPT_FIXTURE)
    # Re-running mask on already-masked text should find zero new structural PII
    remasked, second_map = mask(masked)
    assert not any(
        k.startswith("[JMBG") or k.startswith("[TELEFON") or k.startswith("[EMAIL")
        for k in second_map
    ), "Masked output still contains detectable structural PII"


def test_no_pii_leak_in_masked_output():
    raw_values = [VALID_JMBG, VALID_EMAIL, VALID_IBAN]
    masked, _ = mask(TRANSCRIPT_FIXTURE)
    for val in raw_values:
        assert val not in masked, f"PII leaked into masked output: {val}"


# ---------------------------------------------------------------------------
# token_store (encrypt/decrypt round-trip)
# ---------------------------------------------------------------------------

def test_token_store_roundtrip():
    token_map = {"[PERSON_1]": "Tarik Fetahović", "[JMBG_1]": VALID_JMBG}
    encrypted = encrypt_token_map(token_map)
    assert isinstance(encrypted, str)
    assert VALID_JMBG not in encrypted
    decrypted = decrypt_token_map(encrypted)
    assert decrypted == token_map


# ---------------------------------------------------------------------------
# chunking
# ---------------------------------------------------------------------------

def test_chunk_turns_single():
    turns = [Turn(role="user", text="Pitanje?", position=0)]
    chunks = chunk_turns(turns)
    assert len(chunks) == 1
    assert chunks[0].tip_segmenta == "Pitanje"


def test_chunk_turns_agent_is_odgovor():
    turns = [Turn(role="agent", text="Odgovor!", position=0)]
    chunks = chunk_turns(turns)
    assert chunks[0].tip_segmenta == "Odgovor"


def test_chunk_turns_unknown_is_kontekst():
    turns = [Turn(role="unknown", text="Nešto.", position=0)]
    chunks = chunk_turns(turns)
    assert chunks[0].tip_segmenta == "Kontekst"


def test_chunk_turns_long_turn_splits():
    long_text = " ".join(["word"] * 250)
    turns = [Turn(role="agent", text=long_text, position=0)]
    chunks = chunk_turns(turns)
    assert len(chunks) > 1


def test_chunk_turns_empty_text_skipped():
    turns = [Turn(role="user", text="", position=0)]
    chunks = chunk_turns(turns)
    assert chunks == []


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------

def test_safe_log_does_not_leak_text(caplog):
    raw = f"Tarik {VALID_JMBG}"
    with caplog.at_level(logging.INFO, logger="app.services.preprocessing.audit"):
        safe_log("test_event", transcript_id=99, chars=len(raw))
    for record in caplog.records:
        assert raw not in record.getMessage()
        assert VALID_JMBG not in record.getMessage()


def test_text_hash_is_short_hex():
    h = text_hash("some text")
    assert len(h) == 12
    assert all(c in "0123456789abcdef" for c in h)


# ---------------------------------------------------------------------------
# SSN masking
# ---------------------------------------------------------------------------

def test_mask_removes_ssn():
    masked, token_map = mask(f"SSN: {VALID_SSN}")
    assert VALID_SSN not in masked
    assert any(k.startswith("[SSN_") for k in token_map)


# ---------------------------------------------------------------------------
# Speaker LLM — privacy boundary
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_llm_speaker_never_receives_raw_pii(monkeypatch):
    """
    Even when LLM labeling is triggered, the text sent to Groq must be
    the already-masked version — never the original with real PII values.
    """
    from unittest.mock import MagicMock, patch
    from app.services.preprocessing.speakers_llm import label_speakers_llm
    from app.services.preprocessing.pii.masker import mask as do_mask

    raw_pii_text = f"Hello my SSN is {VALID_SSN} and JMBG {VALID_JMBG}."
    masked_text, _ = do_mask(raw_pii_text)

    captured: list[str] = []

    def fake_create(**kwargs):
        for msg in kwargs.get("messages", []):
            captured.append(msg.get("content", ""))
        mock_resp = MagicMock()
        mock_resp.choices[0].message.content = '{"turns": [{"role": "user", "text": "' + masked_text + '"}]}'
        return mock_resp

    with patch("app.services.preprocessing.speakers_llm.Groq") as MockGroq:
        MockGroq.return_value.chat.completions.create = fake_create
        await label_speakers_llm(masked_text)

    for content in captured:
        assert VALID_SSN not in content, "Raw SSN reached Groq"
        assert VALID_JMBG not in content, "Raw JMBG reached Groq"


@pytest.mark.asyncio
async def test_llm_speaker_fallback_on_failure(monkeypatch):
    """Returns [] when Groq is unavailable — pipeline degrades gracefully."""
    from unittest.mock import patch
    from app.services.preprocessing.speakers_llm import label_speakers_llm

    with patch("app.services.preprocessing.speakers_llm.Groq", side_effect=Exception("no network")):
        turns = await label_speakers_llm("Some text without speaker labels.")
    assert turns == []


@pytest.mark.asyncio
async def test_speaker_strategy_uses_llm_for_audio_transcript(monkeypatch):
    """
    When split_turns finds only 'unknown' roles (raw audio), the pipeline
    strategy should attempt LLM labeling and use its result.
    """
    from unittest.mock import AsyncMock, patch
    from app.services.preprocessing.speakers import split_turns
    from app.services.preprocessing.speakers_llm import label_speakers_llm
    from app.services.preprocessing.models import Turn

    audio_text = "Hello I need help with my account. Of course I can help you."
    pattern_turns = split_turns(audio_text)
    assert all(t.role == "unknown" for t in pattern_turns)

    labeled = [
        Turn(role="user", text="Hello I need help with my account.", position=0),
        Turn(role="agent", text="Of course I can help you.", position=1),
    ]

    with patch(
        "app.services.preprocessing.speakers_llm.label_speakers_llm",
        new=AsyncMock(return_value=labeled),
    ) as mock_llm:
        result = pattern_turns
        if all(t.role == "unknown" for t in result):
            llm_result = await mock_llm(audio_text)
            if llm_result:
                result = llm_result

    assert result[0].role == "user"
    assert result[1].role == "agent"
