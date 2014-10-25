from functools import wraps
from flask import session, redirect, abort
import app.db_funcs.file as f_database
from app.oth_funcs import rnd_funcs
from app.settings import g_vars
import os




def save_file_localy(user_id, opened_file):
    if not opened_file or not user_id: return False

    directory_name = rnd_funcs.get_directory_name()

    user_directory = "user_id_{0}".format(str(user_id))

    file_name = rnd_funcs.get_file_name()

    content_folder = g_vars['content_path']

    local_file_path = os.path.join(user_directory, directory_name, file_name)
    full_path = os.path.join(content_folder, user_directory, directory_name)
    full_file_path = os.path.join(content_folder, user_directory, directory_name, file_name)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    if os.path.exists(os.path.join(full_path, file_name)):
        return save_file_localy(user_id, opened_file)

    opened_file.save(full_file_path)

    return local_file_path




