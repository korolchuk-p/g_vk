from app import app
import json
from flask import Flask, render_template, request, session, redirect, send_file
from werkzeug import  secure_filename
from app.oth_funcs import decorators
import app.db_funcs.main as database
from app.oth_funcs import tokens
from cStringIO import StringIO
from datetime import timedelta


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
        res['error'] = "User not delete"

    return json.dumps(res)

@decorators.logined()
@decorators.token_check()
@app.route('/upload_content', methods=['POST'])
def upload_image():
    res = {}

    content_type = request.form.get('content_type', None)

    g_file = request.files.get('send_file', None)
    second_file_name = request.form.get('file_name', None)
    second_file_name = second_file_name.encode('utf-8') if second_file_name else None

    allowed_image_ext = ['jpg',
                   'jpeg',
                   'png',
                   'ico',
                   'bmp',
                   'gif',
                   'icon']
    allowed_video_ext = ['avi',
                   'wmv',
                   'mp4',
                   'flv',
                   '3gp']

    allowed_text_ext = ['txt',
                   'doc',
                   'xls',
                   'pdf']


    content_type = str(content_type).lower()

    if content_type == 'image':
        allowed_ext = allowed_image_ext
    else:
        if content_type == 'video':
            allowed_ext = allowed_video_ext
        else:
            if content_type == 'text':
                allowed_ext = allowed_text_ext
            else:
                content_type = 'other'

    if not g_file:
        res = {'error': "No file"}
        return json.dumps(res)

    file_ext = g_file.filename.rsplit('.', 1)

    if len(file_ext) > 1:
        file_name = file_ext[0]
        file_ext = file_ext[1]
    else:
        file_name = g_file.filename
        file_ext = ""
    file_ext = file_ext.lower()
    if content_type != 'other' and not (file_ext in allowed_ext):
        res = {'error': "Not available file extension"}
        return json.dumps(res)

    g_filename = secure_filename(g_file.filename)

    f_id = database.set_file(g_file.read().encode('base64'), g_filename)

    if not f_id:
        res = {'error': "Database error"}
        return json.dumps(res)

    user_id = database.get_user_id(session.get('login', None))

    if database.set_user_file_relation(user_id, f_id, content_type, "test"):
        res = {'success': "<a href='/user/file?id={0}'>go</a>".format(str(f_id))}
        return json.dumps(res)


    res = {'error': "Other error"}
    return json.dumps(res)


@app.route('/user/file', methods=['GET'])
def get_user_file():
    file_id = request.args.get('id', None)
    download = "attachment" if request.args.get('dl', None) else "inline"

    if not file_id:
        abort(404)

    resp = database.get_file(file_id)

    if not resp:
        abort(404)

    file_name, file_date = resp
    maked_file = file_date.decode('base64')

    as_open_file = StringIO(maked_file)
    import mimetypes
    mimetypes.init()

    file_ext = file_name.rsplit('.', 1)[1] if len(file_name.rsplit('.', 1)) > 1 else ""
    file_ext = file_ext.lower()

    res = send_file(as_open_file, mimetype=mimetypes.types_map.get('.' + file_ext, 'application/binary'), cache_timeout=timedelta(days=1000).total_seconds())
    res.headers['Content-Disposition'] = download + "; filename ='" + file_name + "'"
    return  res










