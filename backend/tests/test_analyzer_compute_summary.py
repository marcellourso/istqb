from app.analyzer import compute_summary

def test_compute_summary_empty_when_only_whitespace():
    assert compute_summary("   \n\t  ") == ""


def test_compute_summary_returns_first_sentence_prefix_and_excludes_second():
    text = "Prima frase. Seconda frase."
    summary = compute_summary(text)

    assert summary.startswith("Prima frase")
    assert "Seconda frase" not in summary


def test_compute_summary_returns_first_question_prefix_and_excludes_second():
    text = "Prima domanda? Seconda frase."
    summary = compute_summary(text)

    assert summary.startswith("Prima domanda")
    assert "Seconda frase" not in summary


def test_compute_summary_falls_back_to_stripped_prefix_if_no_sentence_break():
    text = "Testo senza punteggiatura di fine frase"
    assert compute_summary(text) == text


def test_compute_summary_is_truncated_to_180_chars():
    text = "A" * 300
    summary = compute_summary(text)
    assert len(summary) == 180
    assert summary == "A" * 180