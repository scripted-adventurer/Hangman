"""A session represents a user's interaction with the application. 
Sessions can contain multiple games, where a game is one word being 
guessed. Sessions can also be shared between users by sharing the encoded 
URL that represents the session. 
"""

import os
import random


class Session:
    """Represents a single session being played by a user.
    """
    def __init__(self, encoded_url=None):
        self.key = os.environ['HANGMAN_KEY']
        self.char_map = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
            'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ','] 
        self.word_table = ["FINESSE", "WHITMAN", "TACONY", "VECCHIO", "PALMYRA", 
        "GOLDEN", "BRIDGE", "NARROWS", "BIFROST"]
        self.previous_word_indexes = []
        self.current_word_index = None
        self.current_word = None
        self.word_display = []
        self.guesses = []
        self.letters_guessed = []
        self.word_guessed = None
        self.errors = []
        self.victory = False
        self.defeat = False
        self.encoded_url = encoded_url
        if encoded_url:
            self.decode_url(encoded_url)

    def decode_url(self, url):
        """Decode and parse the URL, extracting the list of previous words, 
        current word, and guesses.
        """
        decoded = []
        for char_index in range(len(url)):
            char_to_decode = url[char_index]
            char_value = self.char_map.index(url[char_index])
            key_value = self.char_map.index(self.key[char_index])
            decoded_char_value = (char_value - key_value) % 38
            decoded.append(self.char_map[decoded_char_value])
        data = ''.join(decoded).split('-')
        self.previous_word_indexes = [int(digit) for digit in data[0]]
        self.current_word_index = int(data[1])
        self.current_word = self.word_table[self.current_word_index]
        self.guesses = data[2].split(',') if data[2] else []
        for guess in self.guesses:
            if len(guess) > 1:
                self.word_guessed = guess 
            else:
                self.letters_guessed.append(guess)    

    def encode_url(self):
        """Update the encoded URL containing all the game data.
        """
        previous_word_indexes = ''.join([str(i) for i in 
            self.previous_word_indexes])
        current_word_index = str(self.current_word_index)
        guesses = ','.join(self.guesses)
        data_string = (f"{previous_word_indexes}-{current_word_index}-{guesses}")
        encoded = []
        for char_index in range(len(data_string)):
            char_value = self.char_map.index(data_string[char_index])
            key_value = self.char_map.index(self.key[char_index])
            encoded_char_value = (char_value + key_value) % 38
            encoded.append(self.char_map[encoded_char_value])
        self.encoded_url = ''.join(encoded)

    def get_new_word(self):
        """Clear out the guesses, update the previous words list, and 
        update game_data with a new random unplayed word
        """
        self.guesses = []
        if self.current_word_index:
            self.previous_word_indexes.append(self.current_word_index)
        available_words = []
        for word_index in range(9):
            if word_index not in self.previous_word_indexes:
                available_words.append(word_index)
        self.current_word_index = random.choice(available_words)
        self.current_word = self.word_table[self.current_word_index]

    def add_guess(self, guess):
        """Parse the guess and update letter guesses or word guesses as 
        appropriate. 
        """
        guess = guess.upper()
        if len(guess) > 1 and self.word_guessed:
            self.errors.append('You have already guessed a word in this game.')
        elif len(guess) > 1:
            self.guesses.append(guess)
            self.word_guessed = guess
        else:
            self.guesses.append(guess)
            self.letters_guessed.append(guess)

    def update_word_display(self):
        """Add all correctly guessed letters or a word to the display, 
        leaving unguessed letters as _
        """
        if self.word_guessed == self.current_word:
            self.word_display = list(self.current_word)
            return 
        
        self.word_display = []
        for char in self.current_word:
            if char in self.guesses:
                self.word_display.append(char)
            else:
                self.word_display.append('_')

    def undo(self):
        """Remove the previous guess. 
        If there was no previous guess, go to the previous word. 
        If there was no previous word, select a new word.
        """
        if self.guesses:
            self.guesses.pop()
        elif self.previous_word_indexes:
            self.current_word_index = self.previous_word_indexes.pop()
            self.current_word = self.word_table[self.current_word_index]
        else:
            self.current_word_index = random.choice(range(9))
            self.current_word = self.word_table[self.current_word_index]

    def check_game_end(self):
        """Check letters and word guessed to see if all letters/word 
        were correctly guessed, or if 8 incorrect guesses were made.
        """
        self.guesses_left = 8
        letters_to_match = set(list(self.current_word))
        correct_letters = set()
        for letter in self.letters_guessed:
            if letter in letters_to_match:
                correct_letters.add(letter)
            else:
                self.guesses_left -= 1
        if self.word_guessed and (self.word_guessed != self.current_word):
            self.guesses_left -= 1
        if (self.word_guessed == self.current_word or len(letters_to_match) == 
            len(correct_letters)):
            self.victory = True
        elif self.guesses_left <= 0:
            self.defeat = True     

    def get_context(self):
        """Return all the necessary data for rendering the game template
        """
        return {'url': self.encoded_url, 'errors': ' '.join(self.errors), 
            'word_display': ' '.join(self.word_display), 
            'guesses': ' '.join(self.guesses), 'guesses_left': self.guesses_left, 
            'victory': self.victory, 'defeat': self.defeat, 
            'prev_word_count': len(self.previous_word_indexes)}

    def get_encoded_url(self):
        return self.encoded_url  

    def has_errors(self):
        if self.errors:
            return True
        else:
            return False          