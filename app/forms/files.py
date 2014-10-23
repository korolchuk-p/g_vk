from app import app
import json
import os
from flask import Flask, render_template, request, session, redirect, send_file
from werkzeug import  secure_filename
from app.oth_funcs import decorators
import app.db_funcs.main as database
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
    g_filename = secure_filename(g_file.filename)
    file_ext = g_filename.rsplit('.', 1)

    if len(file_ext) > 1:
        file_name = file_ext[0]
        file_ext = file_ext[1]
    else:
        file_name = g_filename
        file_ext = ""

    file_ext = file_ext.lower()
    if content_type != 'other' and not (file_ext in allowed_ext):
        res = {'error': "Not available file extension"}
        return json.dumps(res)


    user_id = database.get_user_id(session.get('login', None))

    file_path = saving.save_file_localy(user_id, g_file)

    f_id = database.set_file(path=file_path, name=g_filename)
    #f_id = database.set_file(g_file.read().encode('base64'), g_filename)

    if not f_id:
        res = {'error': "Database error"}
        return json.dumps(res)



    if database.set_user_file_relation(user_id, f_id, content_type, "test"):
        res = {'success': "/user/file?id={0}".format(str(f_id))}
        return json.dumps(res)


    res = {'error': "Other error"}
    return json.dumps(res)


@app.route('/user/file', methods=['GET'])
def get_user_file():
    file_id = request.args.get('id', None)
    download = "attachment" if request.args.get('dl', None) else "inline"

    print request.headers.get('Range', None)

    if not file_id:
        abort(404)

    resp = database.get_file(file_id)

    if not resp:
        abort(404)

    file_name, source, file_date = resp

    if source == "db":
        maked_file = file_date.decode('base64')
        as_open_file = StringIO(maked_file)
    elif source == "local":
        as_open_file = os.path.join(g_vars['content_path'], file_date)
    else:
        return "error"

    import mimetypes
    mimetypes.init()
    file_ext = file_name.rsplit('.', 1)[1] if len(file_name.rsplit('.', 1)) > 1 else ""
    file_ext = file_ext.lower()

    res = send_file(as_open_file, mimetype=mimetypes.types_map.get('.' + file_ext, 'application/binary'), cache_timeout=timedelta(days=1000).total_seconds())
    res.headers['Content-Disposition'] = download + "; filename ='" + file_name + "'"
    return  res


@app.route('/user/file_stream', methods=['GET'])
def get_user_file_steam():

    ranges = request.headers.get('Range', None)


    file_id = request.args.get('id', None)
    download = "attachment" if request.args.get('dl', None) else "inline"

    if not file_id:
        abort(404)

    resp = database.get_file(file_id)

    if not resp:
        abort(404)

    file_name, source, file_date = resp

    file_size = 0

    if source == "db":
        maked_file = file_date.decode('base64')
        as_open_file = StringIO(maked_file)
        file_size = len(as_open_file)
    elif source == "local":
        as_open_file = os.path.join(g_vars['content_path'], file_date)
        file_size = os.path.getsize(as_open_file)
    else:
        return "error"

    import mimetypes
    mimetypes.init()
    file_ext = file_name.rsplit('.', 1)[1] if len(file_name.rsplit('.', 1)) > 1 else ""
    file_ext = file_ext.lower()

    resp_code = 200


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
            resp_code = 206
    #from flask import Response
    res = send_file(as_open_file, mimetype=mimetypes.types_map.get('.' + file_ext, 'application/binary'), cache_timeout=timedelta(days=1000).total_seconds())

    res.headers['Content-Disposition'] = download + "; filename ='" + file_name + "'"
    if ranges:
        res.headers['Content-Range'] = 'bytes {0}-{1}/{2}'.format(start, end-1, file_size)
        #res.direct_passthrough = True

    res.status_code = resp_code

    res.headers['Accept-Ranges'] = 'bytes'
    return  res
