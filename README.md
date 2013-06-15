
SMB4Manger Samba4 Manager
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**
**Add new lib samba python**

Instalation
====
    ## OpenSUSE 12.X
    zypper install -y gcc make python-xml git-core python-devel python-pip python-virtualenv

    ## Ubuntu/Debian
    apt-get install gcc make git-core python-devel python-pip python-virtualenv

    cd /opt/
    git clone http://github.com/jniltinho/smb4manager.git
    cd smb4manager
    chmod +x create_env.sh
    ./create_env.sh


Run SMB4Manager
====

    ## Production
    ./run.py
    ## Production and Debug
    ./run.py --debug

    http://server_ip:8010
    samba4 administrator login


Screen
====

![image](https://raw.github.com/jniltinho/smb4manager/desenv3/screens/smb4manager_login.png)
![image](https://raw.github.com/jniltinho/smb4manager/desenv3/screens/smb4manager_user_add.png)
![image](https://raw.github.com/jniltinho/smb4manager/desenv3/screens/smb4manager_user_edit.png)
![image](https://raw.github.com/jniltinho/smb4manager/desenv3/screens/smb4manager_users.png)



Requirements
====
samba4, samba-tool, python-xml, git-core, python-pip, python-virtualenv, gcc, make


### Bug, Task, Features Report

* [Bugtracker](https://github.com/jniltinho/smb4manager/issues)
