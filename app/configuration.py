# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, sys
lib_samba = ['/opt/samba4/lib/python2.7/site-packages',
             '/opt/samba4/lib64/python2.7/site-packages',
             '/usr/local/samba/lib/python2.7/site-packages',
             '/usr/local/samba/lib64/python2.7/site-packages'
            ]

for i in lib_samba:
    if (os.path.exists(i)): sys.path.append(i)


class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	DATABASE_URI = 'sqlite:///application.db'
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "MINHACHAVESECRETA"
	CSRF_ENABLED = True
	USERS = {'administrator':'smb4manager', 'linuxpro':'linuxpro12'}



class SMBConfig(Config):
	DEBUG = True
	NOME = "NEW SMB4Manager Flask APP"

