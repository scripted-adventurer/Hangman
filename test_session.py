"""Test all logic in url.py
"""

from session import Session


class TestSession:
    """Test the Session class in session.py
    """

    def test_encode_decode(self):
        """Check that decoding successfully reverses encoding.
        """
        session = Session()
        session.previous_word_indexes = [2, 5]
        session.current_word_index = 7
        session.guesses = ['E', 'T', 'A', 'O', 'BRIDGE', 'I']
        session.encode_url()
        decoded = Session()
        decoded.decode_url(session.encoded_url)

        assert decoded.previous_word_indexes == [2, 5]
        assert decoded.current_word_index == 7
        assert decoded.current_word == 'NARROWS'
        assert decoded.guesses == ['E', 'T', 'A', 'O', 'BRIDGE', 'I']
        assert decoded.letters_guessed == ['E', 'T', 'A', 'O', 'I']
        assert decoded.word_guessed == 'BRIDGE'

    def test_get_new_word(self):
        """Check that guesses are cleared out, previous words are 
        tracked, and game data successfully updates with a new word.
        """
        session = Session()
        session.current_word_index = 7
        session.current_word = 'NARROWS'
        session.guesses = ['E']
        session.get_new_word()
        assert session.current_word != None
        assert session.previous_word_indexes == [7]
        assert session.guesses == []
        session.guesses = ['TEST']
        session.get_new_word()
        assert session.current_word != None
        assert len(session.previous_word_indexes) == 2
        previous_word = session.word_table[session.previous_word_indexes[0]]
        assert session.current_word != previous_word
        assert session.guesses == []

    def test_add_guess(self):
        """Check that both letter and word guesses are correctly tracked, 
        and that only one word guess per game is enforced.
        """
        session = Session()
        assert session.guesses == []
        session.add_guess('E')
        session.add_guess('S')
        assert session.guesses == ['E', 'S']
        assert session.letters_guessed == ['E', 'S']
        assert session.word_guessed == None
        session.add_guess('T')
        session.add_guess('A')
        assert session.guesses == ['E', 'S', 'T', 'A']
        assert session.letters_guessed == ['E', 'S', 'T', 'A']
        assert session.word_guessed == None
        session.add_guess('BRIDGE')
        assert session.guesses == ['E', 'S', 'T', 'A', 'BRIDGE']
        assert session.letters_guessed == ['E', 'S', 'T', 'A']
        assert session.word_guessed == 'BRIDGE'
        session.add_guess('SUCCESS')
        assert session.guesses == ['E', 'S', 'T', 'A', 'BRIDGE']
        assert session.letters_guessed == ['E', 'S', 'T', 'A']
        assert session.word_guessed == 'BRIDGE'
        assert session.errors == ['You have already guessed a word in this game.']

    def test_update_word_display(self):
        """Check that the word display successfully updates in response 
        to guesses.
        """
        session = Session()
        session.current_word = 'TACONY'
        session.guesses.append('E')
        session.letters_guessed.append('E')
        session.guesses.append('S')
        session.letters_guessed.append('S')
        session.update_word_display()
        assert session.word_display == ['_', '_', '_', '_', '_', '_']
        session.guesses.append('T')
        session.letters_guessed.append('T')
        session.guesses.append('A')
        session.letters_guessed.append('A')
        session.update_word_display()
        assert session.word_display == ['T', 'A', '_', '_', '_', '_']
        session.guesses.append('TACONY')
        session.word_guessed = 'TACONY'
        session.update_word_display()
        assert session.word_display == ['T', 'A', 'C', 'O', 'N', 'Y']

    def test_undo(self):
        """Check that undo:
        Returns to a previous guess when available.
        Returns to a previous word when no guesses have been made.
        Picks a new word when no previous words are available.
        """
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('E')
        session.letters_guessed.append('E')
        session.guesses.append('S')
        session.letters_guessed.append('S')
        assert session.guesses == ['E', 'S']
        session.undo()
        assert session.guesses == ['E']
        session.guesses.append('TACONY')
        session.word_guessed = 'TACONY'
        assert session.guesses == ['E', 'TACONY']
        session.undo()
        assert session.guesses == ['E']
        session = Session()
        session.previous_word_indexes = [3, 5]
        session.current_word_index = 1
        session.current_word = 'WHITMAN'
        session.undo()
        assert session.current_word_index == 5
        assert session.current_word == 'GOLDEN'
        assert session.previous_word_indexes == [3]
        session = Session()
        session.current_word_index = 4
        session.current_word = 'PALMYRA'
        session.undo()
        assert session.current_word_index != None
        assert session.current_word != None
        assert session.previous_word_indexes == []

    def test_check_game_end(self):
        """Check that:
        In progress game has neither victory nor defeat
        Correctly guessed word is victory
        Correctly guessed letters is victory
        8 incorrect letter guesses is defeat
        7 incorrect letter guesses, 1 incorrect word guess is defeat
        """
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('V')
        session.letters_guessed.append('V')
        session.guesses.append('E')
        session.letters_guessed.append('E')
        session.guesses.append('C')
        session.letters_guessed.append('C')
        session.guesses.append('H')
        session.letters_guessed.append('H')
        session.guesses.append('I')
        session.letters_guessed.append('I')
        session.check_game_end()
        assert session.guesses_left == 8
        assert session.defeat == False
        assert session.victory == False
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('T')
        session.letters_guessed.append('T')
        session.guesses.append('S')
        session.letters_guessed.append('S')
        session.guesses.append('A')
        session.letters_guessed.append('A')
        session.guesses.append('N')
        session.letters_guessed.append('N')
        session.guesses.append('R')
        session.letters_guessed.append('R')
        session.guesses.append('U')
        session.letters_guessed.append('U')
        session.guesses.append('W')
        session.letters_guessed.append('W')
        session.check_game_end()
        assert session.guesses_left == 1
        assert session.defeat == False
        assert session.victory == False
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('V')
        session.letters_guessed.append('V')
        session.guesses.append('E')
        session.letters_guessed.append('E')
        session.guesses.append('C')
        session.letters_guessed.append('C')
        session.guesses.append('H')
        session.letters_guessed.append('H')
        session.guesses.append('I')
        session.letters_guessed.append('I')
        session.guesses.append('O')
        session.letters_guessed.append('O')
        session.check_game_end()
        assert session.guesses_left == 8
        assert session.defeat == False
        assert session.victory == True
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('VECCHIO')
        session.word_guessed = 'VECCHIO'
        session.check_game_end()
        assert session.guesses_left == 8
        assert session.defeat == False
        assert session.victory == True
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('T')
        session.letters_guessed.append('T')
        session.guesses.append('S')
        session.letters_guessed.append('S')
        session.guesses.append('A')
        session.letters_guessed.append('A')
        session.guesses.append('N')
        session.letters_guessed.append('N')
        session.guesses.append('R')
        session.letters_guessed.append('R')
        session.guesses.append('U')
        session.letters_guessed.append('U')
        session.guesses.append('W')
        session.letters_guessed.append('W')
        session.guesses.append('Z')
        session.letters_guessed.append('Z')
        session.check_game_end()
        assert session.guesses_left == 0
        assert session.defeat == True
        assert session.victory == False
        session = Session()
        session.current_word = 'VECCHIO'
        session.guesses.append('T')
        session.letters_guessed.append('T')
        session.guesses.append('S')
        session.letters_guessed.append('S')
        session.guesses.append('A')
        session.letters_guessed.append('A')
        session.guesses.append('N')
        session.letters_guessed.append('N')
        session.guesses.append('R')
        session.letters_guessed.append('R')
        session.guesses.append('U')
        session.letters_guessed.append('U')
        session.guesses.append('W')
        session.letters_guessed.append('W')
        session.guesses.append('PALMYRA')
        session.word_guessed = 'PALMYRA'
        session.check_game_end()
        assert session.guesses_left == 0
        assert session.defeat == True
        assert session.victory == False