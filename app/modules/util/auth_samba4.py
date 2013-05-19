#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Versao 0.1

import os, sys
import argparse

lib_samba = ['/opt/samba4/lib/python2.7/site-packages', '/usr/local/samba/lib/python2.7/site-packages']

for i in lib_samba:
        if (os.path.exists(i)): sys.path.append(i) 


import samba
import ldb
from samba.dcerpc import samr, security, lsa
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB

lp = param.LoadParm()
lp.load_default()


def _connect(username, password, hostname='localhost'):
      try:
         creds = credentials.Credentials()
         creds.set_username(username)
         creds.set_password(password)
         creds.set_domain("")
         creds.set_workstation("")
         conn = samba.Ldb("ldap://"+ hostname,lp=lp,credentials=creds)
      except Exception, e:
            return False;
      return True;


def main():
        #----------------------------------------
        # parse arguments
        #----------------------------------------
        parser = argparse.ArgumentParser(description='Auth Samba4 Flask App')
        parser.add_argument('--username', dest='smb_user', help='username samba4 requer admin useraname')
        parser.add_argument('--password', dest='smb_pass', help='password for username')
        parser.add_argument('--hostname', dest='smb_hostname', help='hostname default localhost')
        args = parser.parse_args()

        #----------------------------------------
        # get auth samba4
        #----------------------------------------
        if args.smb_user and args.smb_pass:
                retorno = _connect(args.smb_user, args.smb_pass)
                if (retorno): print "Autenticado"


if __name__ == "__main__":
        main()
