import os
import sys

cur_path = os.path.dirname(os.path.realpath(__file__))


wsgi_file_name="run_proj"
apache_conf_file = "/etc/apache2/sites-enabled/site-g_vk.conf"

create_conf_win_files = False
create_conf_lin_files = False

create_log_files = False

create_all_foldes = False

create_wsgi_file = False
create_new = False

add_to_apache = False


if '--linux' in sys.argv: create_conf_lin_files = True
if '--win' in sys.argv: create_conf_win_files = True
if '--log' in sys.argv: create_log_files = True
if '--folders' in sys.argv: create_all_foldes = True
if '--wsgi' in sys.argv: create_wsgi_file = True
if '--apache' in sys.argv: add_to_apache = True
if '--new' in sys.argv: create_new = True

if '--help' in sys.argv or '-h' in sys.argv:
	print """
args:
--help or -h : to show this
--linux : to create *.conf file to apache for linux
--win : to create *.conf file to apache for windows
--log : to create *.log files
--folders : to create all folders of project
--wsgi : to create *.wsgi for project
--new : delete old files before creating new
"""
	sys.exit(0)

folders_list = ['static',
				'static/images',
				'content',
				'static/js',
				'static/css',
				'apache',
				'apache/logs',
				'app',
				'app/views',
				'app/forms',
				'app/db_funcs',
				'app/oth_funcs',
				'app/templates',
				'log']

log_files_list = ['log/events.log',
				  'apache/logs/error.log',
				  'apache/logs/access.log']


apache_win_conf = """
<VirtualHost *:32520>
	ServerName aa.aa.aa

	WSGIScriptAlias / {path}/{wsgi_file}.wsgi
	WSGIScriptReloading On

	<Directory {path}>
		Order deny,allow
		Allow from all
	</Directory>


	LogLevel warn
	CustomLog "{path}/apache/logs/error.log" common

	LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{{Referer}}i\\" \\"%{{User-agent}}i\\""
	TransferLog  {path}/apache/logs/access.log

</VirtualHost>
"""

apache_lin_conf = """
Listen 5001

<Directory   {path}/>
    AllowOverride None
    Require all granted
</Directory>

<VirtualHost *:5001>
	ServerName aa.aa.aa

	WSGIScriptAlias / {path}/{wsgi_file}.wsgi
	WSGIDaemonProcess aa.aa.aa processes=2 threads=25 display-name=%{{GROUP}}
    WSGIProcessGroup aa.aa.aa
	WSGIScriptReloading On

	DocumentRoot {path}

	LogLevel warn
	CustomLog "{path}/apache/logs/error.log" common


	LogFormat "%h %l %u %t \\"%r\\" %>s %b \\"%{{Referer}}i\\" \\"%{{User-agent}}i\\""
	TransferLog  {path}/apache/logs/access.log

</VirtualHost>
"""

def_wsgi = """
import sys, os, logging

sys.path.append('{path}')

logging.basicConfig(stream=sys.stderr)


from app import app as application
import app.all_imports
"""

#defs

def check_create_dir(path):
	full_path = os.path.join(cur_path, path)
	if not os.path.exists(full_path):
		os.mkdir(full_path)
	return

def touch(path):
	full_path = os.path.join(cur_path, path)
	open(full_path, 'a').close()
	return

def delete_file(path):
	full_path = os.path.join(cur_path, path)
	if os.path.exists(full_path):
		os.remove(full_path)
	return


#folders

if create_all_foldes:
	for f in folders_list:
		check_create_dir(f)


#files
if create_log_files:
	if create_new:
		for f in log_files_list:
			delete_file(f)

	for f in log_files_list:
		touch(f)


if create_conf_win_files or create_conf_lin_files:
	delete_file('apache/h.conf')

	full_conf_path = os.path.join(cur_path, 'apache/h.conf')
	if not os.path.exists(full_conf_path):
		to_write = (apache_win_conf if create_conf_win_files else apache_lin_conf).format(path=cur_path, wsgi_file=wsgi_file_name)
		f = open(full_conf_path, 'a')
		f.writelines(to_write)
		f.close()


if create_wsgi_file:
	delete_file('{0}.wsgi'.format(wsgi_file_name))

	full_wsgi_path = os.path.join(cur_path, '{0}.wsgi'.format(wsgi_file_name))
	if not os.path.exists(full_wsgi_path):
		to_write = def_wsgi.format(path=cur_path)
		f = open(full_wsgi_path, 'w')
		f.writelines(to_write)
		f.close()

if add_to_apache:

	if os.path.exists(apache_conf_file):
		os.remove(apache_conf_file)

	if not os.path.exists(apache_conf_file):
		f = open(apache_conf_file, 'w')
		f.writelines("IncludeOptional {path}/apache/h.conf".format(path=cur_path))
		f.close()