from datetime import timedelta, datetime
import json, os
from flask import send_from_directory, session
from app import app

from app.settings import g_vars

@app.route('/static/images/<files>')
def get_img(files):
    return send_from_directory(g_vars['static_images_path'], files)


@app.route('/static/css/<files>')
def get_css(files):
	return send_from_directory(g_vars['static_css_path'], files)

@app.route('/static/js/', defaults={'path': ''})
@app.route('/static/js/<path:path>')
def get_js(path):
    return send_from_directory(g_vars['static_js_path'], path)


