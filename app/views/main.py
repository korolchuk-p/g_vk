from app import app
import json
from flask import Flask, render_template, request, session, redirect, send_file, abort
from werkzeug.datastructures import Headers
from app.oth_funcs import decorators
import app.db_funcs.main as database
from datetime import datetime
from cStringIO import StringIO

@app.route('/')
def index():
    if not 'login' in session:
        return render_template('index.html')

    return redirect('/home')


@app.route('/home')
@decorators.logined()
@decorators.token_check()
def home_page():

    return render_template('home.html', login=session['login'].decode('utf-8'))


@app.route('/logout', methods=['GET'])
@decorators.logined()
def logout():
    session.pop('login', None)
    return redirect('/')

@app.route('/all_users')
@decorators.access(['admin'])
@decorators.token_check()
def users_test():
    user_s = database.all_users()
    return render_template('users.html', users=user_s)




@app.route('/upload_testing')
@decorators.logined()
@decorators.token_check()
def upload_testing():
    files = database.get_list_files_by_login(session.get('login', None))
    if not files:
        files = {}
    return render_template('test_upload.html', user_files=files)




