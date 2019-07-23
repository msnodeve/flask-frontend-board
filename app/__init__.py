"""
    __init__ file
"""

import requests
import jwt
import bcrypt
import json
from http import HTTPStatus
from flask import Flask, render_template, session, request, jsonify
from flask_bootstrap import Bootstrap
from app.constants import USER_NAME, USER_AUTHOR, ENCODE_SECRET_KEY

URL = 'http://localhost:5000'
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
            # register.html 에서 보내준 값을 받아옴
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            repassword = request.form.get('re-password')
            # import pdb; pdb.set_trace()
            # 유효성 검사(추후 문자열 패턴 적용)
            if (len(name) < 4) or (password != repassword):
                return render_template('err_register.html')
            # name, email, password를 post형식으로 요청
            # password = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
            response = requests.post(URL+"/users", headers=HEADERS, data=json.dumps(
                {'name': name, 'email': email, 'password': password}))
            # 요청에 성공했다면 home.html
            if response.status_code == HTTPStatus.OK:
                return render_template('home.html')
            else:
                return render_template('err_register.html')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """ sign in page """
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            response = requests.post(URL+"/user/auth", headers=HEADERS, data=json.dumps(
                {'name' : name, 'password':password}
            ))
            if response.status_code == HTTPStatus.OK:
                response = response.json()
                session['user_name'] = name
                session['user_id'] = response['user']['id']
                session['api_session_token'] = response['access_token']
                session['logged_in'] = True
                return render_template('home.html')
        
        return render_template('login.html')

    @app.route('/board', methods=['GET', 'POST'])
    def board():
        """ board page """
        if request.method=='GET':
            HEADERS = {'Content-Type': 'application/json; charset=utf-8', "Authorization": session['api_session_token']}
            response = requests.get(URL+"/posts", headers=HEADERS)
            if response.status_code == HTTPStatus.OK:
                response = response.json()
                return render_template('board.html', num=len(response), datas=response)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                return render_template('board.html', num=0, datas=response)
            else:
                return render_template('err.html')
        else:
            # 로그인 시확인하게 하기
            return render_template('home.html')

    @app.route('/write', methods=['GET', 'POST'])
    def write():
        if request.method == 'POST':
            title = request.form.get('title')
            body = request.form.get('body')
            response = requests.post(URL+"/posts", headers=HEADERS, data=json.dumps(
                { 'name': session['user_name'], 'title': title, 'body': body, 'author_id': int(session['user_id'])}
            ))
            if response.status_code == HTTPStatus.OK:
                response = requests.get(URL+"/posts", headers=HEADERS).json()
                return render_template('board.html', num=len(response), datas=response)
            else:
                return render_template('err.html')
        return render_template('write.html')

    @app.route('/logout')
    def logout():
        session['logged_in'] = False
        return render_template('home.html')

    @app.route('/story/<int:post_id>', methods=['GET', 'POST'])
    def story(post_id):
        if request.method == 'GET':
            response = requests.get(URL+"/posts/"+str(session['user_id']), headers=HEADERS)
            if response.status_code == HTTPStatus.OK:
                response = response.json()
            return render_template('story.html', resp=response)
        return render_template('err.html')
    return app

# Testcode 가능한가?