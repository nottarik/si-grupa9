# Testing Proof — Sprint 7

## 1. O testiranju u Sprintu 7

Sprint 7 je donio potpunu obnovu preprocessing pipeline-a: granularno razdvajanje logike u zasebne module
(`normalize`, `speakers`, `chunking`, `pii/recognizers`, `pii/masker`, `pii/token_store`, `audit`, `speakers_llm`),
te novi end-to-end integracioni test koji provjerava čitav tok od teksta transkripta do segmenata i Q&A unosa u bazi.

Testovi su pisani u Pythonu koristeći `pytest` i `pytest-asyncio`. Korištena je odvojena SQLite testna baza (ista
infrastruktura kao u Sprintu 6). Unitni testovi ne zahtijevaju bazu i pokrivaju svaki modul u izolaciji; integracioni
test pokreće `run_pipeline()` nad stvarnom testnom bazom.

---

## 2. Funkcionalnosti obuhvaćene testiranjem

| Funkcionalnost | Tip testiranja | Šta je provjereno | Rezultat |
|---|---|---|---|
| Normalizacija teksta | Unit | Uklanjanje rubnih razmaka i `\r\n`, kolapsiranje višestrukih praznih redova, višestruki razmaci u jedan, NFC normalizacija, prazni string | Prošlo |
| Prepoznavanje govornika | Unit | Ispravne role (`agent`/`korisnik`), nepoznati govornik → `unknown`, preskakanje praznih redova, redoslijed pozicija sekvencijalan | Prošlo |
| JMBG checksum validacija | Unit | Ispravan JMBG prolazi checksum, nevaljan (promijenjena posljednja cifra) ne prolazi | Prošlo |
| Detekcija strukturalnog PII | Unit | JMBG, email, telefon, IBAN, SSN se prepoznaju; 13-cifreni broj bez ispravnog checksuma se ne klasifikuje kao JMBG | Prošlo |
| Maskiranje PII | Unit | JMBG/telefon/email/SSN se uklanjaju i zamjenjuju placeholderima; isti PII → isti placeholder; roundtrip obnova; maskirani tekst ne sadrži novo PII (idempotentnost); no-leak test za više vrsta PII | Prošlo |
| Token store | Unit | `encrypt_token_map` / `decrypt_token_map` roundtrip — enkriptovani blob ne sadrži originalne PII vrijednosti | Prošlo |
| Chunking | Unit | Agent turn → `Odgovor`, korisnik turn → `Pitanje`, nepoznati → `Kontekst`; dugački turn se dijeli na više chunkova; prazni turn se preskače (vraća `[]`) | Prošlo |
| Audit logging | Unit | `safe_log` ne propušta ni raw tekst ni PII u logove; `text_hash` vraća 12-znakovni hex string | Prošlo |
| LLM speaker — privatnost | Unit (mock) | Groq API nikad ne prima originalni tekst s PII — prima isključivo maskiranu verziju | Prošlo |
| LLM speaker — fallback | Unit (mock) | Kada Groq nije dostupan (exception), `label_speakers_llm` vraća `[]` bez crash-a | Prošlo |
| LLM speaker — strategija | Unit (mock) | Kada `split_turns` vrati samo `unknown` role (sirovi audio transkript), pipeline poziva LLM labeling i koristi rezultat | Prošlo |
| Pipeline — end-to-end | Integraciono | `run_pipeline()` nad SQLite bazom: maskira PII, kreira ispravne `Segment` zapise, kreira `UnosBazeZnanja` Q&A parove, kreira `TokenMapRecord` — PII se ne pojavljuje ni u jednom od navedenih | Prošlo |

---

## 3. Pokretanje testova

**Komanda:**

```bash
pytest tests/unit/ -v > rezultati.txt 2>&1
```

**Lokacija:** `projekat/backend/`

**Rezultat:**

| | |
|---|---|
| Ukupno testova | 37 |
| Prošlo | 37 |
| Nije prošlo | 0 |
| Greške | 0 |
| Vrijeme | 4.31 s |

**Test fajlovi:**

- `tests/unit/test_preprocessing.py` — 36 testova
- `tests/unit/test_pipeline_integration.py` — 1 test

---

## 4. Kompletan pytest output

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.2.0, pluggy-1.6.0
asyncio: mode=Mode.AUTO
collecting ... collected 37 items

tests/unit/test_preprocessing.py::test_normalize_strips_and_unifies_newlines PASSED          [  3%]
tests/unit/test_preprocessing.py::test_normalize_collapses_blank_lines PASSED                [  5%]
tests/unit/test_preprocessing.py::test_normalize_collapses_spaces PASSED                     [  8%]
tests/unit/test_preprocessing.py::test_normalize_nfc PASSED                                  [ 11%]
tests/unit/test_preprocessing.py::test_normalize_empty PASSED                                [ 14%]
tests/unit/test_preprocessing.py::test_split_turns_roles PASSED                              [ 16%]
tests/unit/test_preprocessing.py::test_split_turns_unknown_fallback PASSED                   [ 19%]
tests/unit/test_preprocessing.py::test_split_turns_empty_lines_skipped PASSED                [ 22%]
tests/unit/test_preprocessing.py::test_split_turns_positions_sequential PASSED               [ 24%]
tests/unit/test_preprocessing.py::test_jmbg_checksum_valid PASSED                           [ 27%]
tests/unit/test_preprocessing.py::test_jmbg_checksum_invalid PASSED                         [ 30%]
tests/unit/test_preprocessing.py::test_find_structural_pii_jmbg PASSED                      [ 32%]
tests/unit/test_preprocessing.py::test_find_structural_pii_email PASSED                     [ 35%]
tests/unit/test_preprocessing.py::test_find_structural_pii_phone PASSED                     [ 38%]
tests/unit/test_preprocessing.py::test_find_structural_pii_iban PASSED                      [ 40%]
tests/unit/test_preprocessing.py::test_find_structural_pii_ssn PASSED                       [ 43%]
tests/unit/test_preprocessing.py::test_jmbg_13_digits_no_checksum_not_detected PASSED       [ 46%]
tests/unit/test_preprocessing.py::test_mask_removes_jmbg PASSED                             [ 49%]
tests/unit/test_preprocessing.py::test_mask_removes_phone PASSED                            [ 51%]
tests/unit/test_preprocessing.py::test_mask_removes_email PASSED                            [ 54%]
tests/unit/test_preprocessing.py::test_mask_same_value_same_placeholder PASSED              [ 57%]
tests/unit/test_preprocessing.py::test_mask_roundtrip PASSED                                [ 59%]
tests/unit/test_preprocessing.py::test_mask_token_map_invertible PASSED                     [ 62%]
tests/unit/test_preprocessing.py::test_no_pii_leak_in_masked_output PASSED                  [ 65%]
tests/unit/test_preprocessing.py::test_token_store_roundtrip PASSED                         [ 68%]
tests/unit/test_preprocessing.py::test_chunk_turns_single PASSED                            [ 70%]
tests/unit/test_preprocessing.py::test_chunk_turns_agent_is_odgovor PASSED                  [ 73%]
tests/unit/test_preprocessing.py::test_chunk_turns_unknown_is_kontekst PASSED               [ 76%]
tests/unit/test_preprocessing.py::test_chunk_turns_long_turn_splits PASSED                  [ 78%]
tests/unit/test_preprocessing.py::test_chunk_turns_empty_text_skipped PASSED                [ 81%]
tests/unit/test_preprocessing.py::test_safe_log_does_not_leak_text PASSED                   [ 84%]
tests/unit/test_preprocessing.py::test_text_hash_is_short_hex PASSED                        [ 86%]
tests/unit/test_preprocessing.py::test_mask_removes_ssn PASSED                              [ 89%]
tests/unit/test_preprocessing.py::test_llm_speaker_never_receives_raw_pii PASSED            [ 92%]
tests/unit/test_preprocessing.py::test_llm_speaker_fallback_on_failure PASSED               [ 95%]
tests/unit/test_preprocessing.py::test_speaker_strategy_uses_llm_for_audio_transcript PASSED [ 97%]
tests/unit/test_pipeline_integration.py::test_run_pipeline_creates_segments_and_qa PASSED   [100%]

======================== 37 passed, 0 warnings in 4.31s ========================
```

---

## 5. Zaključak

Svih 37 novih testova prolazi bez grešaka. Unitni testovi pokrivaju svaki preprocessing modul u izolaciji —
normalizacija, prepoznavanje govornika, detekcija i maskiranje PII za pet tipova entiteta (JMBG, telefon, email, IBAN,
SSN), šifriranje token mape, chunking i audit logging. Tri testa s mockanim Groq klijentom verificiraju privatnosni
boundary LLM speaker labeling-a: originalni PII nikad ne dospijeva do eksternog API-ja. End-to-end integracioni test
potvrđuje da `run_pipeline()` kreira ispravne DB zapise i da niti jedan PII entitet ne curi u maskirani tekst,
segmente ni Q&A unose.
