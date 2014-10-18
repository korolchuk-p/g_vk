from app import app
import json
from flask import Flask, render_template, request, session

import app.db_funcs.main as database

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    login = request.form.get("user", "").encode("utf-8")
    passwd = request.form.get("pass", "").encode("utf-8")

    if not passwd or not login: res = '0'
    if len(login) < 2 or len(passwd) < 2: res = '0'

    if not database.try_login(login, passwd):
        res = '0'
    else:
        session['login'] = login
        res = '1'

    return res

@app.route('/regist', methods=['POST'])
def regitration():
    res = '0'
    login = request.form.get("user", "").encode("utf-8")
    passwd = request.form.get("pass", "").encode("utf-8")
    email = request.form.get("email", "").encode("utf-8")

    if not passwd or not login: res = '0'
    if len(login) < 2 or len(passwd) < 2: res = '0'

    if not database.add_new_user(login, passwd, email): res = '0'
    else: res = '1'

    return res


@app.route('/all_users')
def users_test():

    return json.dumps(database.all_users())
