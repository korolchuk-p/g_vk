import MySQLdb
from app.settings import g_vars
from app.db_funcs import db_con
from app.oth_funcs.logs import add_to_log
#import app.db_funcs.file as f_database



def all_users():
    res = []
    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT `id`, `name`, `access_status` FROM `users`")

    for u in cur.fetchall():
        d = dict()
        d['login'] = u[1].decode("utf-8") if u[1] else ""
        d['id'] = u[0]
        d['status'] = u[2].decode("utf-8") if u[2] else ""
        res.append(d)

    cur.close()
    db.close()

    return  res


def add_new_user(login, passwd, email=""):

    if user_exist(login): return False

    res = False
    db = db_con()
    cur = db.cursor()
    add_to_log("try to create new user = {0}, email = {1}".format(str(login), str(email)))
    cur.execute("INSERT INTO `users` (`name`, `passwd`, `email`, `access_status`) VALUES ('{0}', PASSWORD('{1}'), '{2}', 'user')".format(login, passwd, email))
    db.commit()
    res = True
    cur.close()
    db.close()
    return res


def  user_exist(login):

    res = False
    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT (`id`) FROM `users` WHERE `name`='{0}'".format(login))

    if cur.fetchall(): res = True

    cur.close()
    db.close()

    return  res


def try_login(login, passwd):

    succuss = False

    res = 0

    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT (`id`) FROM `users` WHERE `name`='{0}' AND `passwd`=PASSWORD('{1}')".format(login, passwd))

    a = cur.fetchall()
    if a:
        res = a[0][0]
        succuss = True

    cur.close()
    db.close()

    add_to_log("try to login user = {0}, {1}".format(str(login), "succuss" if succuss else "fail"))
    return  (succuss, res)


def get_user_status(login):

    if not user_exist(login): return False

    db = db_con()
    cur = db.cursor()
    cur.execute("SELECT `access_status` FROM `users` WHERE `name`='{0}'".format(login))
    a = cur.fetchall()
    res = a[0][0] if a else ""
    cur.close()
    db.close()

    return  res


def  get_last_token_by_user(login):

    res = False
    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT (`last_token`) FROM `users` WHERE `name`='{0}'".format(login))
    a = cur.fetchall()
    if a :
        res = a[0][0]

    cur.close()
    db.close()

    return  res


def  set_last_token_by_user(login, token):
    db = db_con()
    cur = db.cursor()

    cur.execute("UPDATE `users` SET `last_token`='{0}' WHERE `name`='{1}'".format(token, login))

    db.commit()
    cur.close()
    db.close()

    return  True


def  del_user_by_name_or_id(user_name=None, user_id=None):
    if not user_name and not user_id: return False

    db = db_con()
    cur = db.cursor()

    cur.execute("DELETE FROM `users` WHERE `name`='{0}' OR `id`='{1}'".format(user_name, user_id))

    db.commit()
    cur.close()
    db.close()

    return  True


def  get_user_id(user_name):

    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT `id` FROM `users` WHERE `name`='{0}'".format(user_name))

    resp = cur.fetchall()

    if not resp: return False

    resp = resp[0][0]

    cur.close()
    db.close()

    return  resp

def get_user_files(user_id=None ,user_name=None):
    if not user_id and not user_name: return False

    db = db_con()
    cur = db.cursor()

    if not user_id:
        user_id = get_user_id(user_name)
        if not user_id: return False


    cur.execute("SELECT `file_id` FROM `rel_user_file` WHERE `user_id` = '{0}'".format(user_id))

    resp = cur.fetchall()

    if not resp: return False
    res = [i[0] for i in resp ]

    cur.close()
    db.close()

    return res


def get_user_by_file(file_id):

    db = db_con()
    cur = db.cursor()


    cur.execute("SELECT `user_id` FROM `rel_user_file` WHERE `file_id` = '{0}'".format(file_id))

    resp = cur.fetchall()

    if not resp: return False
    resp = resp[0][0]

    cur.close()
    db.close()

    return resp
