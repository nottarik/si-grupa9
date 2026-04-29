import pytest
from app.services.pipeline.pipeline_service import PipelineService


def test_normalize_strips_whitespace():
    svc = PipelineService()
    result = svc._normalize("  Hello\r\nWorld  ")
    assert result == "Hello\nWorld"


def test_mask_pii_jmbg():
    svc = PipelineService()
    masked = svc._mask_pii("Moj JMBG je 0101990123456.")
    assert "0101990123456" not in masked
    assert "[JMBG]" in masked


def test_extract_qa_pairs():
    svc = PipelineService()
    segments = [
        {"role": "user", "text": "Kako mogu platiti račun?"},
        {"role": "agent", "text": "Možete platiti putem internet bankarstva."},
        {"role": "user", "text": "Koja je radno vrijeme?"},
        {"role": "agent", "text": "Radimo od 8 do 16 sati."},
    ]
    pairs = svc._extract_qa(segments)
    assert len(pairs) == 2
    assert pairs[0]["question"] == "Kako mogu platiti račun?"
    assert "internet bankarstva" in pairs[0]["answer"]
def test_normalize_empty_string():
    svc = PipelineService()
    result = svc._normalize("")
    assert result == ""


def test_mask_pii_phone():
    svc = PipelineService()
    masked = svc._mask_pii("Moj broj je 061123456.")
    assert "061123456" not in masked


def test_extract_qa_empty():
    svc = PipelineService()
    pairs = svc._extract_qa([])
    assert pairs == []


def test_extract_qa_only_user():
    svc = PipelineService()
    segments = [
        {"role": "user", "text": "Pitanje bez odgovora?"},
    ]
    pairs = svc._extract_qa(segments)
    assert len(pairs) == 0