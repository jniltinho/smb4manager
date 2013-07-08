# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import samba
import logging,sys
from samba.dcerpc import samr, security, lsa,srvsvc
from samba import credentials, param
from samba.samdb import SamDB
from samba import version
from samba.param import LoadParm

from ldb import SCOPE_SUBTREE
from samba.auth import system_session, AUTH_SESSION_INFO_DEFAULT_GROUPS, AUTH_SESSION_INFO_AUTHENTICATED, AUTH_SESSION_INFO_SIMPLE_PRIVILEGES


class AuthSMB4(object):
	def __init__(self,user,password):
		self.user = user
		self.password = password
		_isLastErrorAvailable=False
		self.lp = LoadParm()
		self.lp.load_default()
                self.ip = '127.0.0.1'
                self.WorkGroup = str(self.lp.get("workgroup"))
                self.creds = credentials.Credentials()
                self.creds.set_username(self.user)
                self.creds.set_password(self.password)
                self.creds.set_domain(self.WorkGroup)
                self.creds.set_workstation("")


		self.logger = logging.getLogger(__name__)
		self.logger.addHandler(logging.StreamHandler(sys.stdout))
		self.logger.setLevel(logging.INFO)
		
        def Autenticate(self):
                try:
                        session_info_flags = ( AUTH_SESSION_INFO_DEFAULT_GROUPS | AUTH_SESSION_INFO_AUTHENTICATED )

                        LdapConn = samba.Ldb("ldap://%s" % self.ip,lp=self.lp,credentials=self.creds)
                        DomainDN = LdapConn.get_default_basedn()
                        search_filter="sAMAccountName=%s" % self.user
                        res = LdapConn.search(base=DomainDN, scope=SCOPE_SUBTREE,expression=search_filter, attrs=["dn"])
                        if len(res) == 0:
                                return False

                        user_dn = res[0].dn
                        session = samba.auth.user_session(LdapConn, lp_ctx=self.lp, dn=user_dn,session_info_flags=session_info_flags)
                        token = session.security_token


                        if (token.has_builtin_administrators()):
                                return True

                        if(token.is_system()):
                                return True

                except Exception,e:
                        if(len(e.args)>1):
                                self.logger.info("%s %s" % (e.args[1],e.args[0]))
                                self.SetError(e.args[1],e.args[0])
                        else:
                                self.logger.info("%s " % (e.args[0]))
                                self.SetError(e.args,0)
                return False


	
	def SetError(self,message,number=-1):
		self.LastErrorStr = message
		self.LastErrorNumber = number
		#self.Log.LogError(message)
		self._isLastErrorAvailable=True
			
	def IHaveError(self):
		return self._isLastErrorAvailable



