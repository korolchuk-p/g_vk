from app import app
import json
from flask import Flask, render_template, request, session, redirect
from app.oth_funcs import decorators
import app.db_funcs.main as database
from app.oth_funcs import tokens

@app.route('/login', methods=['POST'])
def login():
    res = {}

    login = request.form.get("user", None)
    login = login.encode("utf-8") if login else login
    passwd = request.form.get("pass", None)
    passwd = passwd.encode("utf-8") if passwd else passwd

    if (not passwd) or (not login):
        res['error'] = 'Login or password empty'
        return json.dumps(res)

    if (len(login) < 2) or (len(passwd) < 2):
        res['error'] = "Login or password haven't right size"
        return json.dumps(res)

    if not database.try_login(login, passwd):
        res['error'] = "Wrong login or password"
    else:
        session['login'] = login
        new_token = tokens.get_token()
        if (database.set_last_token_by_user(login, new_token)):
            session['token'] =  new_token
        res['success'] = ""

    return json.dumps(res)


@app.route('/regist', methods=['POST'])
def regitration():
    res = {}

    login = request.form.get("user", None)
    login = login.encode("utf-8") if login else login

    passwd = request.form.get("pass", None)
    passwd = passwd.encode("utf-8") if passwd else passwd

    email = request.form.get("email", None)
    email = email.encode("utf-8") if email else ""

    if (not passwd) or (not login):
        res['error'] = 'Login or password empty'
        return json.dumps(res)

    if (len(login) < 2) or (len(passwd) < 2):
        res['error'] = "Login or password haven't right size"
        return json.dumps(res)

    if not database.add_new_user(login, passwd, email):
        res['error'] = "User already exists"
    else:
        res['success'] = ""

    return json.dumps(res)

@app.route('/login_check', methods=['POST'])
def login_check():
    res = {}

    login = request.form.get("user", None)
    login = login.encode("utf-8") if login else login

    if not login:
        res['error'] = 'Login empty'
        return json.dumps(res)

    if len(login) < 2:
        res['error'] = "Login hasn't right size"
        return json.dumps(res)

    if database.user_exist(login):
        res['error'] = "Login already exists"
    else:
        res['success'] = ""

    return json.dumps(res)






