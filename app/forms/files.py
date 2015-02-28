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

@decorators.logined()
@decorators.token_check()
@app.route('/upload_content', methods=['POST'])
def upload_image():
    res = {}

    content_type = request.form.get('content_type', None)

    g_file = request.files.get('send_file', None)

    file_secure = request.form.get('secure', 'all')

    second_file_name = request.form.get('file_name', None)
    second_file_name = second_file_name.encode('utf-8') if second_file_name else None

    allowed_ext = g_vars['allowed_ext']

    if not g_file:
        res = {'error': "No file"}
        return json.dumps(res)

    content_type = str(content_type).lower()

    g_filename = secure_filename(g_file.filename)
    file_ext = g_filename.rsplit('.', 1)

    if len(file_ext) > 1:
        file_name = file_ext[0]
        file_ext = file_ext[1]
    else:
        file_name = g_filename
        file_ext = ""
    file_ext = file_ext.lower()

    if content_type not in allowed_ext.keys():
        content_type = 'other'
    else:
        if not (file_ext in allowed_ext.get(content_type, "")):
            res = {'error': "Not available file extension"}
            return json.dumps(res)


    user_id = u_database.get_user_id(session.get('login', None))

    file_path = saving.save_file_localy(user_id, g_file)
    link = rnd_funcs.get_file_link()
    while not f_database.check_link(link):
        link = rnd_funcs.get_file_link()

    f_id = f_database.set_file(path=file_path, name=g_filename, link=link, secure=file_secure, file_type=content_type)

    if not f_id:
        res = {'error': "Database error"}
        return json.dumps(res)

    if f_database.set_user_file_relation(user_id, f_id):
        res = {'success': "/file/{0}".format(link)}
        return json.dumps(res)


    res = {'error': "Other error"}
    return json.dumps(res)


@app.route('/file/', defaults={'path':''})
@app.route('/file/<path:path>', methods=['GET'])
def get_file(path):

    ranges = request.headers.get('Range', None)

    download = "attachment" if request.args.get('dl', None) else "inline"

    if not path:
        abort(404)

    resp = f_database.get_file(link=path)

    if not resp:
        abort(404)

    file_name, file_path, file_type, secure, file_link, file_id, file_added = resp

    ## secure =!!
    as_open_file = os.path.join(g_vars['content_path'], file_path)
    file_size = os.path.getsize(as_open_file)

    import mimetypes
    mimetypes.init()
    file_ext = file_name.rsplit('.', 1)[1] if len(file_name.rsplit('.', 1)) > 1 else ""
    file_ext = file_ext.lower()

    start = end = None

    if ranges:
        parts = ranges.split('=', 1)[1] if len(ranges.split('=', 1)) > 1 else None
        if parts:
            parts = parts.replace(' ', '').split('-')
            start = int(parts[0]) if parts[0] else 0
            end = int(parts[1]) if parts[1] else file_size
            if not isinstance(as_open_file, InputType):
                f = open(as_open_file, 'rb')
            else:
                f = as_open_file
            f.seek(start)
            as_open_file = f.read(end - start)
            as_open_file = StringIO(as_open_file)
            f.close()

    res = send_file(as_open_file, mimetype=mimetypes.types_map.get('.' + file_ext, 'application/binary'), cache_timeout=timedelta(days=1000).total_seconds())

    res.headers['Content-Disposition'] = download + "; filename ='" + file_name + "'"
    if ranges:
        res.headers['Content-Range'] = 'bytes {0}-{1}/{2}'.format(start, end - 1, file_size)
        #res.direct_passthrough = True

    res.status_code = 200 if not ranges else 206

    res.headers['Accept-Ranges'] = 'bytes'
    return  res

@decorators.logined()
@decorators.token_check()
@decorators.access(['admin', 'user'])
@app.route('/delete_file/', defaults={'path':''})
@app.route('/delete_file/<path:path>', methods=['GET'])
def delete_file(path):
    if not path: abort(404)

    resp = f_database.get_file(link=path)

    if not resp:
        abort(404)
    user_status = u_database.get_user_status(session.get('login', None))
    file_name, file_path, file_type, secure, file_link, file_id, file_added = resp
    if not (user_status in ['admin']):
        user_id = u_database.get_user_by_file(file_id)
        if user_id != session.get('id', None):
            return abort(403)

    os.remove(os.path.join(g_vars['content_path'], file_path))
    f_database.del_user_file_relation(file_id=file_id)
    f_database.del_file(file_id)

    return json.dumps({'success': ''})
