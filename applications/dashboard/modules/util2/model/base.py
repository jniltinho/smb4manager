
import samba
import ldb
from samba.dcerpc import samr, security, lsa
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB

from  adsbrowser.lib.Logs import AppLog

class BaseModel:
	lp = param.LoadParm()
	lp.load_default()
	creds=None
	LdapConn=None
	auth_success=False
	_isLastErrorAvailable=False
	LastErrorStr='';
	LastErrorNumber=0;
	RootDSE='' 
	DnsDomain='' 
	schemaNamingContext='' 
	Log = AppLog();
	
	def __init__(self,username,password):
		self.username=username;
		self.password=password;
		if self._connect():
			self._GetBase();

	def _connect(self):
		try:
			
			self.creds = credentials.Credentials()
			self.creds.set_username(self.username)
			self.creds.set_password(self.password)
			#self.creds.set_domain("SAMDOM")
			self.creds.set_domain("")
			self.creds.set_workstation("")
			self.LdapConn = samba.Ldb("ldap://127.0.0.1",lp=self.lp,credentials=self.creds)
			self.samrpipe = samr.samr("ncalrpc:", self.lp, self.creds)
			self.connect_handle = self.samrpipe.Connect(None, security.SEC_FLAG_MAXIMUM_ALLOWED)			
		except ldb.LdbError, (num, msg):
			self.SetError(msg,num)
			return False;
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		else:
			if not self.creds.is_anonymous():
				self.auth_success = True;
			else:
				self.SetError('No esta permitido el bindeo anonimo',0)
				return False;
				
		return True;
		
		
	def isAuthenticate(self):
		return self.auth_success;

	def _GetBase(self):
		if(self.isAuthenticate()):
			try:
				LdapSearchResult = self.LdapConn.search("", scope=ldb.SCOPE_BASE, attrs=["namingContexts", "defaultNamingContext", "schemaNamingContext","configurationNamingContext","ldapServiceName"])
				#self.RootDSE = LdapSearchResult[0]["defaultNamingContext"];
				self.RootDSE = str(self.LdapConn.get_root_basedn());
				self.DnsDomain = str(LdapSearchResult[0]["ldapServiceName"]).split(':')[0];
				self.schemaNamingContext = LdapSearchResult[0]["schemaNamingContext"][0];
			except ldb.LdbError, (num, msg):
				self.SetError(msg,num)
				return False;
			except Exception,e:
				self.SetError(e.message,0)
				return False;
			else:
				return True;
		else:
			self.SetError('Error de autenticacion',0)
			return False;

	def SetError(self,message,number):
		self.LastErrorStr = message;
		self.LastErrorNumber = number;
		self.Log.LogError(message);
		self._isLastErrorAvailable=True;
			
	def IHaveError(self):
		return self._isLastErrorAvailable;




