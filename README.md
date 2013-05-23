
smb4manager Framework Flask
===========

Samba4 Web Manager

**Webapp for manager Samba4 samba-tool**
**Do not use in production environment**
**Add new lib samba python**

Instalation
====
    ## OpenSUSE 12.X
    zypper install -y gcc make python-xml git-core python-pip python-virtualenv

    ## Ubuntu/Debian
    apt-get install gcc make python-xml git-core python-pip python-virtualenv

    cd /opt/
    git clone -b desenv3 http://github.com/jniltinho/smb4manager.git
    cd smb4manager
    chmod +x create_env.sh
    ./create_env.sh


Run SMB4Manager
====

    ## Prod
    ./run.py --prod
    ## For Debug
    ./run.py --prod --debug

    https://server_ip:8010
    Login: administrator
    Pass: smb4manager


Screen
====

![image](https://raw.github.com/jniltinho/smb4manager/master/screens/smb4manager.png)


Requirements
====
samba4, samba-tool, python-xml, git-core, python-pip, python-virtualenv, gcc, make


### Bug, Task, Features Report

* [Bugtracker](http://linuxpro.com.br/bugtracker/)
