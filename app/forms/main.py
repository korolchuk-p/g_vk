from app import app
import json
import os
from flask import Flask, render_template, request, session, redirect, send_file, abort
from werkzeug import  secure_filename
from app.oth_funcs import decorators
import app.db_funcs.user as u_database
import app.db_funcs.file as f_database
from app.oth_funcs import saving
from app.oth_funcs import rnd_funcs
from cStringIO import StringIO, InputType
from datetime import timedelta
from app.settings import g_vars


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

    (success, user_id) = u_database.try_login(login, passwd)
    if not success:
        res['error'] = "Wrong login or password"
    else:
        session['login'] = login
        session['id'] = user_id
        new_token = rnd_funcs.get_token()
        if (u_database.set_last_token_by_user(login, new_token)):
            session['token'] = new_token
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

    if not u_database.add_new_user(login, passwd, email):
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

    if u_database.user_exist(login):
        res['error'] = "Login already exists"
    else:
        res['success'] = ""

    return json.dumps(res)














