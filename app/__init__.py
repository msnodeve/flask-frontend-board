"""
    __init__ file
"""
import requests, json
from app.constants import USERS_URL,BASE_HEADERS,USERS_AUTH_URL, POSTS_URL,POST_URL
from http import HTTPStatus
from flask import Flask, render_template, request,session

def create_app() -> (Flask):
    """ create_app()을 호출하여 app을 초기화 """
    app = Flask(__name__)
    app.secret_key = 'sec_keys'
    app.app_context().push()
    
    app.config['DEBUG'] = True

    @app.route('/')
    def index():
        if session.get('logged_in'):
            return render_template('index.html', user_id=session['user_id'])
        else:
            return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            user_id = request.form.get('id')
            user_email = request.form.get('email')
            user_password = request.form.get('password')
            user_repassword = request.form.get('re-password')
            if (len(user_id) < 4) or (user_password != user_repassword):
                return render_template('err_register.html')
            data = json.dumps({'user_id': user_id, 'user_email': user_email, 'user_password': user_password})
            response = requests.post(USERS_URL, headers=BASE_HEADERS, data=data)
            if response.status_code == HTTPStatus.OK:
                return render_template('ok_register.html', user_id=user_id)
            return render_template('register.html')
        return render_template('register.html')


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method=='POST':
            user_id = request.form.get('id')
            user_password = request.form.get('password')
            data = json.dumps({'user_id': user_id, 'user_password': user_password})
            response = requests.post(USERS_AUTH_URL, headers=BASE_HEADERS, data=data)
            if response.status_code == HTTPStatus.OK:
                response = response.json()
                session['user_num'] = response['user']
                session['user_id'] = user_id
                session['api_session_token'] = response['access_token']
                session['logged_in'] = True
                return render_template('index.html', user_id=user_id)
            else:
                return render_template('err_login.html')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session['logged_in']=False
        session.pop('user_num', None)
        session.pop('user_id', None)
        session.pop('api_session_token', None)
        return render_template('index.html')

    @app.route('/board')
    def board():
        response = requests.get(POSTS_URL, headers=BASE_HEADERS)
        if response.status_code == HTTPStatus.OK:
            response = response.json()
            return render_template('board.html', num=len(response), posts=response)
        else:
            return render_template('board.html', num=0, posts=response)

    @app.route('/write', methods=['GET', 'POST'])
    def write():
        if session.get('logged_in'):
            if request.method=='POST':
                title = request.form.get('title')
                body = request.form.get('body')
                HEADERS = {'Content-Type': 'application/json; charset=utf-8', "Authorization": session['api_session_token']}
                data=json.dumps({ 'user_id': session['user_id'], 'title': title, 'body': body, 'author_id': session['user_id']})
                response = requests.post(POSTS_URL, headers=HEADERS, data=data)
                if response.status_code == HTTPStatus.OK:
                    response = requests.get(POSTS_URL, headers=BASE_HEADERS).json()
                    return render_template('board.html', num=len(response), posts=response)
                else:
                    return render_template('err_board.html')
            else:
                return render_template('write.html')
        else:
            return render_template('err_board.html')

    @app.route('/story/<int:post_id>', methods=['GET', 'POST'])
    def story(post_id):
        HEADERS = {'Content-Type': 'application/json; charset=utf-8', "Authorization": session['api_session_token']}
        response = requests.get(POST_URL+str(post_id), headers=HEADERS)
        if response.status_code == HTTPStatus.OK:
            response = response.json()
            return render_template('story.html', resp=response)
        else:
            return render_template('story.html')
    return app
