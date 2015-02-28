g_vk
====

test social network

Run commands:

sudo chmod +x install_packages.sh 

sudo ./install_packages.sh 

sudo python create_all_folders.py --folders --wsgi --linux --log --apache 

sudo python app/settings.py 

Configure: app/settings.conf 

In mysql:
mysql> create database g_vk;

In console:
sudo mysql -u root -p<passwd> -h localhost g_vk < g_vk.sql-dump
