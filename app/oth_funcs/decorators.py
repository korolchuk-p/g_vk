from functools import wraps
from flask import session, redirect, abort
import app.db_funcs.main as database

def logined():
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):

            if 'login' in session:
                return f(*args, **kwargs)
            else:
                return redirect('/')

        return func

    return decorator


def access(groups=[]):
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):

            login = session.get('login', "")
            if not database.user_exist(login): abort(403)

            user_status = database.get_user_status(login)

            if user_status in groups:
                return f(*args, **kwargs)
            else:
                abort(403)

        return func

    return decorator


