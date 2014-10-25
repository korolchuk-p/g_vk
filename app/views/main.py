from app import app
import json
from flask import Flask, render_template, request, session, redirect, send_file, abort
from werkzeug.datastructures import Headers
from app.oth_funcs import decorators
import app.db_funcs.file as f_database
import app.db_funcs.user as u_database
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
    session.pop('id', None)
    return redirect('/')


@app.route('/upload_testing')
@decorators.logined()
@decorators.token_check()
def upload_testing():

    file_ids = u_database.get_user_files(user_name=session.get('login', None))
    if not file_ids:
        file_ids = []

    files = []
    for i in file_ids:
        file_name, file_path, file_type, secure, file_link, file_id, file_added  = f_database.get_file(f_id=i)
        files.append({'file_name':file_name,
                      'file_path':file_path,
                      'file_type':file_type,
                      'secure':secure,
                      'file_link':file_link,
                      'file_id':file_id,
                      'file_added':file_added})

    return render_template('test_upload.html', user_files=files)




