"""Contains logic for the main application.
"""

import os
import random

from flask import Flask, request, render_template, redirect

from session import Session


def create_app(testing=False):
    app = Flask(__name__)
            
    @app.route('/', methods=['GET'])
    def home():
        """Start a new session
        """
        session = Session()
        session.get_new_word()
        session.encode_url()

        return redirect(f"/session/{session.get_encoded_url()}")

    @app.route('/session/<game_info>/games', methods=['POST'])
    def new_word(game_info):
        """Start a new game (using the specified session).
        """
        session = Session(game_info)
        session.get_new_word()
        session.encode_url()

        return redirect(f"/session/{session.get_encoded_url()}")

    @app.route('/session/<game_info>/guesses', methods=['POST'])
    def guess(game_info):
        """Enter a guess (letter or word) for the game in the specified 
        session.
        """
        session = Session(game_info)
        session.add_guess(request.form['guess'])
        session.encode_url()

        if session.has_errors():
            session.update_word_display()
            session.check_game_end()
            return render_template('base.html', **session.get_context())
        else:
            return redirect(f"/session/{session.get_encoded_url()}")

    @app.route('/session/<game_info>/undo', methods=['POST'])
    def undo(game_info):
        """Go back one step in the game in the specified session.
        """
        session = Session(game_info)
        session.undo()
        session.encode_url()

        return redirect(f"/session/{session.get_encoded_url()}")       

    @app.route('/session/<game_info>', methods=['GET'])
    def load_game(game_info):
        """Load the game using the data specified in the URL
        """
        session = Session(game_info)
        session.update_word_display()
        session.check_game_end()
        session.encode_url()

        return render_template('base.html', **session.get_context())

    return app

if __name__ == '__main__':
    app.run(host='172.17.0.2')