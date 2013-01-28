smb4manager
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**

Instalation
====
    OpenSUSE 12.2

    zypper install -y python-xml python-ldap python-simplejson git

    cd /opt/
    git clone https://github.com/jniltinho/smb4manager.git
    cd smb4manager
    chmod +x start_ssl.sh


Configure
====
    Rename file site-packages/smb4config/smb4config_sample.py to site-packages/smb4config/smb4config.py
    Change config dict in file site-packages/smb4config/smb4config.py
    start web2py in ssl, execute:
    ./start_ssl.sh


Usage
====
    https://server_ip:8010
    Login: admin
    Pass: smb4manager


Screen
====

![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager.png)


Requer
====
samba4, samba-tool


Task Open
====
Users list
Users add
Users del
