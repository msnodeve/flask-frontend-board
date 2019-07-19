"""
    __init__ file
"""

import requests
import json
from flask import Flask, render_template, session, request
from flask_bootstrap import Bootstrap
from app.constants import STATUS_CODE

URL = 'http://localhost:5000/users'
HEADERS = {'Content-Type': 'application/json; charset=utf-8'}


def create_app() -> (Flask):
    """ init app """
    app = Flask(__name__)
    app.app_context().push()
    app.secret_key = "123"
    app.config['DEBUG'] = True
    Bootstrap(app)

    @app.route('/')
    def home():
        """ main page """
        #session['logged_in'] = False
        if session.get('logged_in'):
            return render_template('home.html')
        else:
            return render_template('home.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """ register page """
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            repassword = request.form.get('re-password')
            if (len(name) < 4) or (password != repassword):
                return render_template('register.html')

            response = requests.post(URL, headers=HEADERS, data=json.dumps(
                {'name': name, 'email': email, 'password': password}))

            if response.status_code == STATUS_CODE.CREATED:
                return render_template('home.html')
            else:
                return render_template('register.html')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ sign in page """

        return render_template('login.html')

    return app
