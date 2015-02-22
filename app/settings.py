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

default_config = """main_path:/var/www/g_vk
mysql_passwd:1234
mysql_user:root
mysql_database:g_vk
mysql_server:localhost
audio_files:['mp3', 'ogg','mka', 'wma', 'flac', 'mp4', 'wav']
image_files:['jpg', 'jpeg', 'png', 'ico', 'bmp', 'gif', 'icon']
video_files:['avi', 'wmv', 'mp4', 'flv', '3gp', 'mkv']
text_files:['txt', 'doc', 'xls', 'pdf']
"""

path_to_file = os.path.join(os.path.dirname(__file__), "settings.conf")

if (not os.path.exists(path_to_file)):
    c_file = open(path_to_file, "wt")
    c_file.writelines(default_config)
    c_file.close()

c_file = open(path_to_file, "rt")
g_vars = config_parser(c_file)
c_file.close()


def parse_list(s):
    return [ i for i in s.replace(' ', '').replace("'", '').replace('[', '').replace(']', '').split(',')]

g_vars['allowed_ext'] = {}
g_vars['allowed_ext']['image'] = parse_list(g_vars['image_files'])
g_vars['allowed_ext']['video'] = parse_list(g_vars['video_files'])
g_vars['allowed_ext']['audio'] = parse_list(g_vars['audio_files'])
g_vars['allowed_ext']['text'] = parse_list(g_vars['text_files'])


g_vars['templates_path'] = os.path.join(g_vars['main_path'], 'app/templates')
g_vars['logs_path'] = os.path.join(g_vars['main_path'], "log/events.log")
g_vars['static_images_path'] = os.path.join(g_vars['main_path'], "static/images")
g_vars['static_css_path'] = os.path.join(g_vars['main_path'], "static/css")
g_vars['static_js_path'] = os.path.join(g_vars['main_path'], "static/js")
g_vars['content_path'] = os.path.join(g_vars['main_path'], "content")
