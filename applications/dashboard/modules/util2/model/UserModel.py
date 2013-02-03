import base64
import time
from pylons import response
from adsbrowser.model.base import *;



class UserModel(BaseModel):

	def EnableAccount(self,dn,username,enable=True):
		if not self.isAuthenticate():
			self.SetError('Usted no esta autenticado',0)
			return False;
		try:
			#response.write(str(sys.modules.keys()));
			dn = ldb.Dn(self.LdapConn,dn);
			res = self.LdapConn.search(base=dn, scope=ldb.SCOPE_BASE,attrs=["userAccountControl"])
			if len(res) == 0:
				raise Exception('Unable to find user "%s"' % username)
			assert(len(res) == 1)
			user_dn = res[0].dn
			userAccountControl = int(res[0]["userAccountControl"][0])
			
			
			if(enable):
				if userAccountControl & 0x2:
					# remove disabled bit
					userAccountControl = userAccountControl & ~0x2
				if userAccountControl & 0x20:
					# remove 'no password required' bit
					userAccountControl = userAccountControl & ~0x20
			else:
					userAccountControl = userAccountControl | 0x2


			mod = """
dn: %s
changetype: modify
replace: userAccountControl
userAccountControl: %u
""" % (user_dn, userAccountControl)
			self.LdapConn.modify_ldif(mod)

		except ldb.LdbError, (num, msg):
			self.SetError(msg,num)
			return False;
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True


		
		
	def ForcePasswordChangeAtNextLogin(self,dn,username):
		if not self.isAuthenticate():
			self.SetError('Usted no esta autenticado',0)
			return False;
			
		try:
			dn = ldb.Dn(self.LdapConn,dn);
			res = self.LdapConn.search(base=dn, scope=ldb.SCOPE_BASE,attrs=[])
			if len(res) == 0:
				raise Exception('Unable to find user "%s"' % username)
			assert(len(res) == 1)
			user_dn = res[0].dn
			userAccountControl = int(res[0]["userAccountControl"][0])

			mod = """
dn: %s
changetype: modify
replace: pwdLastSet
pwdLastSet: 0
""" % (user_dn)
			self.LdapConn.modify_ldif(mod)

		except ldb.LdbError, (num, msg):
			self.SetError(msg,num)
			return False;
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True



	def SetPassword(self,dn,username,password):
		if not self.isAuthenticate():
			self.SetError('Usted no esta autenticado',0)
			return False;
			
		try:
			self.LdapConn.transaction_start()
			dn = ldb.Dn(self.LdapConn,dn);
			res = self.LdapConn.search(base=dn, scope=ldb.SCOPE_BASE,attrs=[])
			if len(res) == 0:
				raise Exception('Unable to find user "%s"' % username)
			assert(len(res) == 1)
			user_dn = res[0].dn
			userAccountControl = int(res[0]["userAccountControl"][0])

			mod = """
dn: %s
changetype: modify
replace: unicodePwd
unicodePwd:: %s
""" % (user_dn, base64.b64encode(("\"" + password + "\"").encode('utf-16-le')))
			self.LdapConn.modify_ldif(mod)

		except ldb.LdbError, (num, msg):
			self.SetError(msg,num)
			return False;
		except Exception,e:
			self.LdapConn.transaction_cancel()
			self.SetError(e.message,0)
			return False;
		else:
			self.LdapConn.transaction_commit()
			return True


	def SetExpiry(self,dn,username,days=15,no_expiry_req=False):
		if not self.isAuthenticate():
			self.SetError('Usted no esta autenticado',0)
			return False;
			
		try:
			expiry_seconds = days*24*3600;
			
			self.LdapConn.transaction_start()
			dn = ldb.Dn(self.LdapConn,dn);
			res = self.LdapConn.search(base=dn, scope=ldb.SCOPE_BASE,attrs=["userAccountControl", "accountExpires"])
			if len(res) == 0:
				raise Exception('Unable to find user "%s"' % username)
			assert(len(res) == 1)
			user_dn = res[0].dn

			userAccountControl = int(res[0]["userAccountControl"][0])
			accountExpires = int(res[0]["accountExpires"][0])
			if no_expiry_req:
				userAccountControl = userAccountControl | 0x10000
				accountExpires = 0
			else:
				userAccountControl = userAccountControl & ~0x10000
				accountExpires = samba.unix2nttime(expiry_seconds + int(time.time()))


			mod = """
dn: %s
changetype: modify
replace: userAccountControl
userAccountControl: %u
replace: accountExpires
accountExpires: %u
""" % (user_dn, userAccountControl, accountExpires)
			self.LdapConn.modify_ldif(mod)

		except ldb.LdbError, (num, msg):
			self.LdapConn.transaction_cancel()
			self.LastErrorStr = msg;
			self.LastErrorNumber = num;
			self.Log.LogError(self.LastErrorStr);
			self._isLastErrorAvailable=True;
			return False;
		except Exception,e:
			self.LdapConn.transaction_cancel()
			self.SetError(e.message,0)
			return False;
		else:
				self.LdapConn.transaction_commit()
		#response.write(samba.unix2nttime(299044800))
		#response.write(samba.nttime2string(119435184000000000))
		return True
