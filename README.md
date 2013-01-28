smb4manager
===========

Samba4 Web Manager


**Webapp for manager Samba4 samba-tool**



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
    Configure file site-packages/smb4config/smb4config.py
    ./start_ssl.sh


Usage
====
    https://server_ip:8010
    Login: admin
    Pass: smb4manager
