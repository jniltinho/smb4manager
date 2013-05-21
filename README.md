smb4manager
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**
**Add new lib samba python**

Instalation
====
    ## OpenSUSE 12.2
    zypper install -y python-xml git-core

    ## Ubuntu
    apt-get install git-core

    cd /opt/
    git clone -b desenv http://github.com/jniltinho/smb4manager.git
    cd smb4manager
    cp applications/dashboard/smb4config_sample.ini applications/dashboard/smb4config.ini
    chmod +x start_ssl.sh
    ./start_ssl.sh


Configure
====
    ## Change config applications/dashboard/smb4config.ini
    ## start web2py in ssl, execute:
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
