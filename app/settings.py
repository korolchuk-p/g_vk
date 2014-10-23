import os

def config_parser(f):
    res = {}
    lines = f.readlines()
    for l in lines:
        pa = [p for p in l.replace('\r\n', '').replace('\n', '').split(':')]
        if len(pa)>1:
            key = pa[0]
            value = ''.join(( pa[i] for i in range(len(pa)) if i>0 ))
            res[key] = value

    return res

default_config = """main_path:/home/w123/proj/g_vk
mysql_passwd:123456
mysql_user:root
mysql_database:g_vk
mysql_server:localhost
"""
path_to_file = os.path.join(os.path.dirname(__file__), "paths.conf")

if (not os.path.exists(path_to_file)):
    c_file = open(path_to_file, "wt")
    c_file.writelines(default_config)
    c_file.close()

c_file = open(path_to_file, "rt")
g_vars = config_parser(c_file)
c_file.close()

g_vars['templates_path'] = os.path.join(g_vars['main_path'], 'app/templates')
g_vars['logs_path'] = os.path.join(g_vars['main_path'], "log/events.log")
g_vars['static_images_path'] = os.path.join(g_vars['main_path'], "static/images")
g_vars['static_css_path'] = os.path.join(g_vars['main_path'], "static/css")
g_vars['static_js_path'] = os.path.join(g_vars['main_path'], "static/js")
g_vars['content_path'] = os.path.join(g_vars['main_path'], "content")
