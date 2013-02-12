smb4manager
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**
**Add new lib samba python**

Instalation
====
    OpenSUSE 12.2

    zypper install -y python-xml git

    cd /opt/
    git clone http://github.com/jniltinho/smb4manager.git
    cd smb4manager
    chmod +x start_ssl.sh


Configure
====
    Rename file: applications/dashboard/smb4config_sample.ini
    to: applications/dashboard/smb4config.ini
    Change config applications/dashboard/smb4config.ini
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
    Users edit
