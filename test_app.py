"""Test all logic in app.py
"""

import pytest

from app import create_app
from session import Session


@pytest.fixture
def client():
    app = create_app(testing=True)

    yield app.test_client()

def test_new_game_empty(client):
    """Check that a random word is picked.
    """
    response = client.get('/', follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: ' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_new_game_previous_words(client):
    """Check that a new random word is picked.
    """
    session = Session()
    session.previous_word_indexes = [1]
    session.current_word_index = 2
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/games', 
        follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: ' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_new_game_all_words_guessed(client):
    """Check that the 'New Game' button does not display.
    """
    session = Session()
    session.previous_word_indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    session.current_word_index = 8
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'BIFROST'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'B I F R O S T' in response.data
    assert b'Guesses: BIFROST' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' not in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_word_incorrect(client):
    """Check that guesses are updated correctly.
    """
    session = Session()
    session.current_word_index = 3
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'PALMYRA'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _ _' in response.data
    assert b'Guesses: PALMYRA' in response.data 
    assert b'Guesses left: 7' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_word_twice(client):
    """Check that an error is displayed.
    """
    session = Session()
    session.current_word_index = 2
    session.guesses = ['GOLDEN']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'BRIDGE'}, follow_redirects=True)
    print(response.data)
    assert b'You have already guessed a word in this game.' in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: GOLDEN' in response.data 
    assert b'Guesses left: 7' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_guess_word_incorrect_last_guess(client):
    """Check for defeat.
    """
    session = Session()
    session.current_word_index = 0
    session.guesses = ['G', 'A', 'O', 'U', 'R', 'T', 'W']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'WHITMAN'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: G A O U R T W WHITMAN' in response.data 
    assert b'Guesses left: 0' in response.data
    assert b'<input type="submit" value="Go">' not in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_word_correct(client):
    """Check for victory.
    """
    session = Session()
    session.current_word_index = 1
    session.guesses = ['A', 'I', 'T']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'WHITMAN'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' in response.data
    assert b'Defeat' not in response.data
    assert b'W H I T M A N' in response.data
    assert b'Guesses: A I T WHITMAN' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' not in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' in response.data 

def test_guess_letter_correct(client):
    """Check that guesses and word display are updated correctly.
    """
    session = Session()
    session.current_word_index = 4
    session.guesses = ['A']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'R'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ A _ _ _ R A' in response.data
    assert b'Guesses: A R' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_letter_incorrect(client):
    """Check that guesses are updated correctly.
    """
    session = Session()
    session.current_word_index = 5
    session.guesses = ['E', 'O']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'A'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ O _ _ E _' in response.data
    assert b'Guesses: E O A' in response.data 
    assert b'Guesses left: 7' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_letter_again(client):
    """Check that nothing happens.
    """
    session = Session()
    session.current_word_index = 6
    session.guesses = ['E', 'A', 'R', 'S', 'T']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'R'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ R _ _ _ E' in response.data
    assert b'Guesses: E A R S T' in response.data 
    assert b'Guesses left: 5' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_guess_letter_incorrect_last_guess(client):
    """Check for defeat.
    """
    session = Session()
    session.current_word_index = 7
    session.guesses = ['E', 'A', 'T', 'C', 'R', 'I', 'H', 'P', 'M']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'L'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' in response.data
    assert b'_ A R R _ _ _' in response.data
    assert b'Guesses: E A T C R I H P M' in response.data 
    assert b'Guesses left: 0' in response.data
    assert b'<input type="submit" value="Go">' not in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data

def test_guess_final_letter_correct(client):
    """Check for victory.
    """
    session = Session()
    session.current_word_index = 8
    session.guesses = ['E', 'A', 'I', 'S', 'T', 'O', 'R', 'P', 'B']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/guesses', 
        data={'guess': 'F'}, follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' in response.data
    assert b'Defeat' not in response.data
    assert b'B I F R O S T' in response.data
    assert b'Guesses: E A I S T O R P B F' in response.data 
    assert b'Guesses left: 5' in response.data
    assert b'<input type="submit" value="Go">' not in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' in response.data

def test_undo_at_beginning(client):
    """Check that a new word is picked.
    """
    session = Session()
    session.current_word_index = 2
    session.guesses = []
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/undo', 
        follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: ' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_undo_letter_guess(client):
    """Check that guesses updates correctly.
    """
    session = Session()
    session.current_word_index = 2
    session.guesses = ['E', 'A', 'I', 'S', 'T']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/undo', 
        follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ A _ _ _ _' in response.data
    assert b'Guesses: E A I S' in response.data 
    assert b'Guesses left: 5' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_undo_word_guess(client):
    """Check that guesses updates correctly.
    """
    session = Session()
    session.current_word_index = 3
    session.guesses = ['E', 'A', 'I', 'S', 'T', 'BRIDGE']
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/undo', 
        follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ E _ _ _ I _' in response.data
    assert b'Guesses: E A I S T' in response.data 
    assert b'Guesses left: 5' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data 

def test_undo_no_guesses(client):
    """Check to go back to previous word.
    """
    session = Session()
    session.previous_word_indexes = [4, 2]
    session.current_word_index = 7
    session.encode_url()
    encoded_url = session.get_encoded_url()
    response = client.post(f'/session/{encoded_url}/undo', 
        follow_redirects=True)
    assert b'<div id="error-box">' not in response.data
    assert b'Victory!' not in response.data
    assert b'Defeat' not in response.data
    assert b'_ _ _ _ _ _' in response.data
    assert b'Guesses: ' in response.data 
    assert b'Guesses left: 8' in response.data
    assert b'<input type="submit" value="Go">' in response.data
    assert b'<input type="submit" value="Undo">' in response.data
    assert b'<input type="submit" value="New Game">' not in response.data     