"""The base Controller API

Provides the BaseController class for subclassing.
"""

import json
import samba
import ldb
from samba.dcerpc import samr, security, lsa
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB


class BaseController():

	AuthErr = {"success": False, "msg": 'Usted no esta autenticado'};
	successOK = {'success': True}
	lp = param.LoadParm()
	lp.load_default()
	def __init__(self):
		response.headers['Content-type'] = 'text/javascript; charset=utf-8'
		#response.write(self.__class__);


	def index(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
		else:	
			return json.dumps(self.successOK);

	def _check_session(self):
		if not 'username' in session:
			#response.write('False');
			return False;	
		return True;

	def _connect(self):
		try:
			username = session['username'];
			password = session['password'];
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
