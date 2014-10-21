import MySQLdb
from app.settings import g_vars
from app.oth_funcs.logs import add_to_log

# TOOLS BEGIN
def db_con():
    return MySQLdb.connect( host=g_vars['mysql_server'],
                            user=g_vars['mysql_user'],
                            passwd=g_vars['mysql_passwd'],
                            db=g_vars['mysql_database'] )


def to_utf8(obj):
    return obj.encode('utf-8')

# TOOLS END










# USERS BEGIN
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


def add_new_user(login=None, passwd=None, email=""):
    if not login or not passwd: return False

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


def  user_exist(login=None):
    if not login: return False

    res = False
    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT (`id`) FROM `users` WHERE `name`='{0}'".format(login))

    if cur.fetchall(): res = True

    cur.close()
    db.close()

    return  res


def try_login(login=None, passwd=None):
    if not login or not passwd: return False

    res = False
    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT (`id`) FROM `users` WHERE `name`='{0}' AND `passwd`=PASSWORD('{1}')".format(login, passwd))

    if cur.fetchall(): res = True

    cur.close()
    db.close()

    add_to_log("try to login user = {0}, {1}".format(str(login), "succuss" if res else "fail"))
    return  res


def get_user_status(login):
    if not login: return False
    if not user_exist(login): return False

    db = db_con()
    cur = db.cursor()
    cur.execute("SELECT `access_status` FROM `users` WHERE `name`='{0}'".format(login))
    a = cur.fetchall()
    res = a[0][0] if a else ""
    cur.close()
    db.close()

    return  res


def  get_last_token_by_user(login=None):
    if not login: return False

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


def  set_last_token_by_user(login=None, token=None):
    if not login or not token: return False

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


def  get_user_id(user_name=None):
    if not user_name: return False

    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT `id` FROM `users` WHERE `name`='{0}'".format(user_name))

    resp = cur.fetchall()
    if not resp: return False

    resp = resp[0][0]

    cur.close()
    db.close()

    return  resp


# USERS END












# FILES BEGIN

def set_file(f=None, name=None):
    if not f or not name: return False

    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `files` (`filename`, `data`) VALUES  ('{0}', '{1}')".format(name, f))
    cur.execute("SELECT LAST_INSERT_ID()")
    file_id = cur.fetchall()[0][0]
    db.commit()
    cur.close()
    db.close()

    return file_id


def get_file(f_id):
    if not f_id: return False

    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT `filename`, `data` FROM `files` WHERE `id` = '{0}'".format(f_id))
    resp = cur.fetchall()
    if not resp: return False
    file_data = resp[0][1]
    file_name = resp[0][0]

    cur.close()
    db.close()

    return (file_name, file_data)


def set_user_file_relation(user_id, file_id, file_type="data", category=""):
    if not user_id or not file_id: return False

    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `rel_user_file` (`user_id`, `file_id`, `type`, `category`) VALUES ({0}, {1}, '{2}', '{3}')".format(user_id, file_id, file_type, category))

    db.commit()
    cur.close()
    db.close()

    return True

def get_list_files_by_login(user_name=None):
    if not user_name:
        return False

    db = db_con()
    cur = db.cursor()

    user_id = get_user_id(user_name)
    if not user_id: return False

    cur.execute("SELECT `file_id`, `type`, `category` FROM `rel_user_file` WHERE `user_id` = '{0}'".format(user_id))

    resp = cur.fetchall()

    if not resp: return False
    res = [{'id': i[0], 'type':i[1], 'category':i[2]} for i in resp ]

    cur.close()
    db.close()

    return res

# FILES END
