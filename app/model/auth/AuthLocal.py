


import samba
from ldb import SCOPE_SUBTREE
from AuthBase import AuthBase
from samba.auth import AUTH_SESSION_INFO_DEFAULT_GROUPS, AUTH_SESSION_INFO_AUTHENTICATED, AUTH_SESSION_INFO_SIMPLE_PRIVILEGES 


class AuthLocal(AuthBase):
	def __init__(self,creds,ip):
		
		user = creds.get_username()
		password = creds.get_password()
		
		AuthBase.__init__(self,user,password)
		self.ip = ip
		self.creds = creds
		#self.logger.info("%s %s" % (self.user,self.password))

	def Autenticate(self):
		try:
			session_info_flags = ( AUTH_SESSION_INFO_DEFAULT_GROUPS | AUTH_SESSION_INFO_AUTHENTICATED )
			# When connecting to a remote server, don't look up the local privilege DB
			#if self.url is not None and self.url.startswith('ldap'):
			#	session_info_flags |= AUTH_SESSION_INFO_SIMPLE_PRIVILEGES

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
