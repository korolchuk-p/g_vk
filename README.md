g_vk
====

test social network


run command
sudo python create_all_folders.py --folders --wsgi --linux --log

make file /etc/apache2/sites-available/site-g_vk.conf and insert: 
IncludeOptional /var/www/g_vk/apache/h.conf

In mysql:
mysql> create database g_vk;

In console:
sudo mysql -u root -p<passwd> -h localhost g_vk < g_vk.sql-dump
