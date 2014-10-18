import os



g_vars = dict()
g_vars['main_path'] = "/home/w123/proj/g_vk"
g_vars['templates_path'] = os.path.join(g_vars['main_path'], 'app\\templates')
g_vars['logs_path'] = os.path.join(g_vars['main_path'], "log\\events_log.log")

g_vars['static_images_path'] = os.path.join(g_vars['main_path'], "static\\images")
g_vars['static_css_path'] = os.path.join(g_vars['main_path'], "static\\css")
g_vars['static_js_path'] = os.path.join(g_vars['main_path'], "static\\js")

g_vars['mysql_passwd'] = "123456"
g_vars['mysql_user'] = "root"
g_vars['mysql_database'] = "g_vk"
g_vars['mysql_server'] = "localhost"
