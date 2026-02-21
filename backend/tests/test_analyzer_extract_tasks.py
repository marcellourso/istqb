from app.analyzer import extract_tasks


def test_extract_tasks_extracts_dash_and_todo_lines_and_ignores_empty():
    text = """
    Intro

    - comprare latte
    -    pagare bolletta

    TODO:chiamare il dentista
    todo:prenotare revisione

    -
    TODO:
    TODO:    

    Altro testo
    """

    assert extract_tasks(text) == [
        "comprare latte",
        "pagare bolletta",
        "chiamare il dentista",
        "prenotare revisione",
    ]

def test_extract_tasks_extracts_dash_and_todo_lines():
    text = """
Intro
 
- comprare latte
-    pagare bolletta
 
TODO: chiamare il dentista
todo: mandare email
 
-     
TODO:    
 
Altro testo
"""
 
    assert extract_tasks(text) == [
        "comprare latte",
        "pagare bolletta",
        "chiamare il dentista",
        "mandare email",
    ]
 
 
def test_extract_tasks_does_not_match_todo_with_space_before_colon():
    text = """
TODO : non dovrebbe essere preso
TODO: questo sì
"""
 
    assert extract_tasks(text) == ["questo sì"]
 
 
def test_extract_tasks_ignores_dash_not_at_start_of_line():
    text = """
questa riga - non è un task
 - questo invece sì (c'è un trattino a inizio riga dopo strip)
"""
 
    assert extract_tasks(text) == ["questo invece sì (c'è un trattino a inizio riga dopo strip)"]
