"""The base Controller API

Provides the BaseController class for subclassing.
"""

import sys
# Find right direction when running from source tree
sys.path.insert(0, "/opt/samba4/lib/python2.7/site-packages")


import samba
import ldb
from samba.dcerpc import samr, security, lsa
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB


class BaseController():

	lp = param.LoadParm()
	lp.load_default()


	def _connect(self):
		try:
			username = 'administrator'
			password = 'Criare744512'
			creds = credentials.Credentials()
			creds.set_username(username)
			creds.set_password(password)
			#creds.set_domain("SAMDOM")
			creds.set_domain("")
			creds.set_workstation("")
			self.conn = samba.Ldb("ldap://127.0.0.1",lp=self.lp,credentials=creds)
		except Exception,e:
				raise
		return True;
