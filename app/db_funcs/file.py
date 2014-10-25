import MySQLdb
from app.settings import g_vars
from app.oth_funcs.logs import add_to_log
from app.db_funcs import db_con
from datetime import datetime
#import app.db_funcs.users as u_database
#import app.db_funcs.user as u_database
#import users as u_database
#import app.db_funcs.user as u_database


#file



def set_file(path,  name, link, file_type="others", secure="all", added=datetime.now()):

    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `files` (`filename`, `path`, `link`, `type`, `secure`, `date_added`)"
                " VALUES  ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(name, path, link, file_type, secure, added))

    cur.execute("SELECT LAST_INSERT_ID()")
    file_id = cur.fetchall()[0][0]
    db.commit()
    cur.close()
    db.close()

    return file_id


def get_file(f_id=None, link=None):
    if not link and not f_id: return False

    db = db_con()
    cur = db.cursor()
    if link:
        cur.execute("SELECT `filename`, `path`, `type`, `secure`, `link`, `id`, `date_added`"
                    " FROM `files` WHERE `link` = '{0}'".format(link))
    else:
        cur.execute("SELECT `filename`, `path`, `type`, `secure`, `link`, `id`, `date_added`"
                    " FROM `files` WHERE `id` = '{0}'".format(f_id))
    resp = cur.fetchall()
    if not resp: return False

    secure = resp[0][3]
    file_type = resp[0][2]
    file_path = resp[0][1]
    file_name = resp[0][0]
    file_link = resp[0][4]
    file_id = resp[0][5]
    file_added = resp[0][6]

    cur.close()
    db.close()

    return (file_name, file_path, file_type, secure, file_link, file_id, file_added)

def del_file(file_id):

    db = db_con()
    cur = db.cursor()

    cur.execute("DELETE FROM `files` WHERE `id`={0}".format(file_id))

    db.commit()
    cur.close()
    db.close()

    return True


#rel



def set_user_file_relation(user_id, file_id):

    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `rel_user_file` (`user_id`, `file_id`) VALUES ({0}, {1})".format(user_id, file_id))
    cur.execute("SELECT LAST_INSERT_ID()")
    rel_id = cur.fetchall()[0][0]
    db.commit()
    cur.close()
    db.close()

    return rel_id

def del_user_file_relation(file_id):
    db = db_con()
    cur = db.cursor()

    cur.execute("DELETE FROM `rel_user_file` WHERE `file_id`={0}".format(file_id))

    db.commit()
    cur.close()
    db.close()

    return True


#link




def check_link(link):

    db = db_con()
    cur = db.cursor()

    cur.execute("SELECT `id` FROM `files` WHERE `link`='{0}'".format(link))
    resp = cur.fetchall()
    if resp:
        return resp[0][0]

    cur.close()
    db.close()

    return True
