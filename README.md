
smb4manager Framework Flask
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**
**Add new lib samba python**

Instalation
====
    OpenSUSE 12.X

    zypper install -y python-xml git-core python-gunicorn python-Flask

    cd /opt/
    git -b desenv3 clone http://github.com/jniltinho/smb4manager.git
    cd smb4manager
    chmod +x create_env.sh
    ./create_env.sh


Usage
====
    ./start_ssl.sh
    https://server_ip:8010
    Login: admin
    Pass: smb4manager


Screen
====

![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager.png)


Requirements
====
samba4, samba-tool, python-xml, git-core, python-gunicorn, python-Flask


### Bug,Task,Features Report

* [Bugtracker](http://linuxpro.com.br/bugtracker/).
