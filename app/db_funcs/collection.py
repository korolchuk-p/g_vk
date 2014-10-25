import MySQLdb
from app.settings import g_vars
from app.oth_funcs.logs import add_to_log
from app.db_funcs import db_con
from datetime import datetime
#import app.db_funcs.users as u_database
#import app.db_funcs.user as u_database
#import users as u_database
#import app.db_funcs.user as f_database

def get_collections(collection_id):

    db = db_con()
    cur = db.cursor()


    cur.execute("SELECT `name`, `type`, `date_added`, `secure` FROM `files` WHERE `id`='{0}'".format(collection_id))
    resp = cur.fetchall()
    if not resp: return False
    collection_name = resp[0][0]
    collection_type = resp[0][1]
    collection_added = resp[0][2]
    collection_secure = resp[0][3]

    cur.close()
    db.close()

    return (collection_name, collection_type, collection_added, collection_secure)


def add_collection(user_id, name, c_type="others", secure="all", added=datetime.now()):

    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `collections` (`name`, `type`, `date_added`, `secure`)"
                " VALUES  ('{0}', '{1}', '{2}', '{3}')".format(name, c_type, added, secure))

    cur.execute("SELECT LAST_INSERT_ID()")
    collection_id = cur.fetchall()[0][0]
    if not collection_id: return False

    rel_id = add_rel_collection(use, collection_id)
    if not rel_id: return False

    db.commit()
    cur.close()
    db.close()

    return collection_id


def add_rel_collection(user_id, collection_id):
    db = db_con()
    cur = db.cursor()

    cur.execute("INSERT INTO `rel_user_collection` (`user_id`, `collection_id`"
                " VALUES  ({0}, {1})".format(user_id, collection_id))

    cur.execute("SELECT LAST_INSERT_ID()")
    rel_id = cur.fetchall()[0][0]

    db.commit()
    cur.close()
    db.close()

    return rel_id



