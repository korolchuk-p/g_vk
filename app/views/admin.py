from app import app
import json
from flask import Flask, render_template, request, session, redirect, send_file, abort
from werkzeug.datastructures import Headers
from app.oth_funcs import decorators
import app.db_funcs.user as u_database
from datetime import datetime
from cStringIO import StringIO

@app.route('/all_users')
@decorators.access(['admin'])
@decorators.token_check()
def users_test():
    user_s = u_database.all_users()
    return render_template('users.html', users=user_s)
