from app.analyzer import compute_priority

def test_compute_priority_high_when_contains_urgente():
    assert compute_priority("È URGENTE fare subito") == "high"


def test_compute_priority_high_when_contains_asap_case_insensitive():
    assert compute_priority("please do this asap") == "high"


def test_compute_priority_medium_when_contains_importante():
    assert compute_priority("IMPORTANTE: verifica budget") == "medium"


def test_compute_priority_low_when_no_keywords():
    assert compute_priority("Testo normale senza parole chiave") == "low"


def test_compute_priority_high_has_precedence_over_importante():
    # URGENTE/ASAP vince su IMPORTANTE
    assert compute_priority("IMPORTANTE ma URGENTE") == "high"

