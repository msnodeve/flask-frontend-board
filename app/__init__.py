"""
    __init__ file
"""

from flask import Flask, render_template


def create_app() -> (Flask):
    """ init app """
    app = Flask(__name__)
    app.app_context().push()
    app.config['DEBUG'] = True

    @app.route('/')
    def home():
        """ main page """
        return "Home!"

    return app
