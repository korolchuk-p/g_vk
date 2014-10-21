import sys
from app.settings import g_vars

sys.path.append(g_vars['main_path'])
sys.path.append(g_vars['templates_path'])

from app import app as application
import app.all_imports

import app.db_funcs.main

##


from app.db_funcs import main as dbs


# db_1 = dbs.db_con()
# cur = db_1.cursor()

# #cur.execute("LOCK TABLES `users` WRITE")
# for i in xrange(1000000):
#     cur.execute("INSERT INTO `users` (`name`, `passwd`, `email`, `access_status`) VALUES ('{0}', PASSWORD('{1}'), '{2}', 'user')".format("ololshka_user_#" + str(i), "2222331", "lox1", "user"))
#     if i % 1000 == 0 :
#         print str(i)
#         if i % 10000 == 0:
#             db_1.commit()
# #cur.execute("UNLOCK TABLES")
# db_1.commit()

# cur.close()
# db_1.close()






##

if __name__ == "__main__":
    pass
    application.run(debug=True)


