import sys
from app.settings import g_vars

sys.path.append(g_vars['main_path'])
sys.path.append(g_vars['templates_path'])

from app import app as application
import app.all_imports

import app.db_funcs.main

##


from app.db_funcs import main as dbs

if __name__ == "__main__":
    pass
    application.run(debug=True)


