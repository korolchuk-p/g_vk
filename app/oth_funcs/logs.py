from datetime import timedelta, datetime
import os

from app.settings import g_vars


def get_logfile():
    f = open(g_vars['logs_path'], "a")
    return f


def add_to_log(mes):
    f = get_logfile()
    f.write(str(datetime.now()) +": " + str(mes) + "\n")
    f.close()
    return True
