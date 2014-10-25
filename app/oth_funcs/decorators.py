from functools import wraps
from flask import session, redirect, abort
import app.db_funcs.user as u_database

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
            if not u_database.user_exist(login): abort(403)

            user_status = u_database.get_user_status(login)

            if user_status in groups:
                return f(*args, **kwargs)
            else:
                abort(403)

        return func

    return decorator


def token_check():
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):

            login = session.get('login', None)
            token = session.get('token', None)

            if not (not token or not login):
                if u_database.get_last_token_by_user(login) == token:
                    return f(*args, **kwargs)

            session.pop('login', None)
            session.pop('token', None)
            return redirect('/')

        return func

    return decorator


