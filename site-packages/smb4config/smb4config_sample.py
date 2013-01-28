#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Rename Change smb4config_sample.py to smb4config.py
Change config dict

'''


## Config XMLRPCSERVER API
SERVER   = dict(

host     = '0.0.0.0',
port     =  8910,
keyfile  = 'privatekey.pem',
certfile = 'cert.pem',
users    = {"admin":"123456","admin2":"samba12345"},

)


## Config SAMBA4 SERVER
SAMBA4   = dict(

conf     = '/usr/local/samba/etc/smb.conf',
domain   = 'dominio.local',
admin    = 'administrator',
passwd   = 'Dominio1234', 
hostname = 'dc01.dominio.local', 

smbtool  = '/usr/local/samba/bin/samba-tool',
smblib   = '/usr/local/samba/lib/python2.7/site-packages',

)


