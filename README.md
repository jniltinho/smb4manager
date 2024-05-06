SMB4Manger Samba4 Manager
===========

Samba4 Web Manager

**Webapp to manage Samba4 samba-tool**

Installation
====

    ## Ubuntu/Debian
    apt-get install gcc make git python3-dev python3-pip python3-virtualenv samba

    cd /opt/
    git clone http://github.com/jniltinho/smb4manager.git
    cd smb4manager && bash create_env.sh


ScreenCast
====
* [Youtube](https://www.youtube.com/watch?v=iK73rl2rvSs)


Run SMB4Manager
====

    ## Rocket Standalone WebServer WSGI
    ## Production run SSL
    flask/bin/python3 runserver.py --flask
    https://server_ip:8010
    samba4 administrator login

    ## Debug run SSL
    flask/bin/python3 runserver.py --flask --debug
    https://server_ip:8010
    samba4 administrator login


Screen Shots
====

![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager_login.png)
![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager_dashboard.png)
![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager_user_add.png)
![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager_user_edit.png)
![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager_users.png)



Requirements
====
samba, python3-xmlschema, git, python3-pip, python3-virtualenv, gcc, make


### Bug, Task, Features Report

* [Bugtracker](https://github.com/jniltinho/smb4manager/issues)
