# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
Create KEY

import hashlib
hashlib.md5("Flask_SMB4Manager").hexdigest()
068c2a771435c5c48fdf4a1cd9dfa465
"""

from datetime import timedelta

import os, sys
lib_samba = ['/opt/samba4/lib/python2.7/site-packages',
             '/opt/samba4/lib64/python2.7/site-packages',
             '/usr/local/samba/lib/python2.7/site-packages',
             '/usr/local/samba/lib64/python2.7/site-packages'
            ]

for i in lib_samba:
    if (os.path.exists(i)): sys.path.append(i)


_basedir     = os.path.abspath(os.path.dirname(__file__))
NOME         = "NEW SMB4Manager Flask APP"
DEBUG        = False
TESTING      = False
SECRET_KEY   = '068c2b781435c5c48fdf4a1cd9dfa465' 
CSRF_ENABLED = True
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)

