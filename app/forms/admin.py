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

@decorators.access(['admin'])
@app.route('/admin_tools/del_user', methods=['POST'])
def del_user():
    res = {}

    user_login = request.form.get("user", None)
    user_login = user_login.encode("utf-8") if user_login else user_login

    user_id = request.form.get("id", None)

    if not user_login and not user_id:
        res['error'] = 'Login and id is empty'
        return json.dumps(res)

    if user_login:
        user_id = ""
    else:
        user_login = ""

    if database.del_user_by_name_or_id(user_login, user_id):
        res['success'] = ""
    else:
        res['error'] = "User not deleted"

    return json.dumps(res)

