import MySQLdb
from app.settings import g_vars

def db_con():
    return MySQLdb.connect( host=g_vars['mysql_server'],
                            user=g_vars['mysql_user'],
                            passwd=g_vars['mysql_passwd'],
                            db=g_vars['mysql_database'] )


def to_utf8(obj):
    return obj.encode('utf-8')
