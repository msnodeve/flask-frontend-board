"""
    __init__ file
"""

from flask import Flask, render_template

def create_app() -> (Flask):
    """ create_app()을 호출하여 app을 초기화 """
    app = Flask(__name__)
    app.app_context().push()
    
    app.config['DEBUG'] = True

    @app.route('/')
    def index():
        return render_template('index.html')

    return app