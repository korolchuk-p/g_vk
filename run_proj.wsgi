
import sys, os, logging

sys.path.append('/var/www/g_vk')

logging.basicConfig(stream=sys.stderr)


from app import app as application
import app.all_imports
