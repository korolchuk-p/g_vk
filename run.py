import sys
from app.settings import g_vars

sys.path.append(g_vars['main_path'])
sys.path.append(g_vars['templates_path'])

from app import app as application
import app.all_imports

if __name__ == "__main__":
	application.run(debug=True)


