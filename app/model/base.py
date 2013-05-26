


import samba
import ldb
import logging,sys
from samba.dcerpc import samr, security, lsa,srvsvc
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB
from samba import version
from samba.param import LoadParm


class BaseModel:
	lp = param.LoadParm()
	lp.load_default()
	WorkGroup = str(lp.get("workgroup"))
	Realm = str(lp.get("realm"))
	creds=None
	LdapConn=None
	auth_success=False
	_isLastErrorAvailable=False
	AuthUnix=False
	AuthLocal=False
	AuthRemote=False
	LastErrorStr='';
	LastErrorNumber=0;
	RootDSE='' 
	DnsDomain=Realm 
	schemaNamingContext='' 
	server_address='127.0.0.1'
	SambaVersion = version

	
	def __init__(self,username=None,password=None,AuthMethod="local"):
		self.username=username;
		self.password=password;
		self.AuthMethod=AuthMethod;

                self.logger = logging.getLogger(__name__)
                self.logger.addHandler(logging.StreamHandler(sys.stdout))
                self.logger.setLevel(logging.INFO)
		
		self.Authenticate()


	def Authenticate(self):
		if ((self.username != None) and (self.password !=None)):
			self.creds = credentials.Credentials()
			self.creds.set_username(self.username)
			self.creds.set_password(self.password)
			self.creds.set_domain(self.WorkGroup)
			self.creds.set_workstation("")

			if (self.AuthMethod=="local"):
				from auth.AuthLocal import AuthLocal
				AuthMechanism = AuthLocal(self.creds,self.server_address)
				if AuthMechanism.Autenticate():
					if self._connect():
						self._GetBase();
						self._GetDomainNames();
						self._SetCurrentDomain(0);
						self.AuthLocal = True
						self.auth_success = True
					
				

	def _connect(self):
		try:
			#self.LdapConn = samba.Ldb("ldap://%s" % self.server_address,lp=self.lp,credentials=self.creds)
			self.samrpipe = samr.samr("ncalrpc:%s"% self.server_address, self.lp, credentials=self.creds)
			#self.srvsvcpipe = srvsvc.srvsvc('ncalrpc:%s' % self.server_address,credentials=self.creds)
			#self.connect_handle = self.samrpipe.Connect(None, security.SEC_FLAG_MAXIMUM_ALLOWED)			
			self.connect_handle = self.samrpipe.Connect2(None, security.SEC_FLAG_MAXIMUM_ALLOWED)
		except ldb.LdbError, (num, msg):
			self.SetError(msg,num)
			return False;
		except Exception,e:
			if(len(e.args)>1):
				self.logger.info("%s %s" % (e.args[1],e.args[0]))
				self.SetError(e.args[1],e.args[0])
			else:
				self.logger.info("%s %s" % (e.args[0],"Error"))
				self.SetError(e.args,0)
			return False;
		else:
			if not self.creds.is_anonymous():
				self.auth_success = True;
			else:
				self.SetError("self.Lang.AnonymousAuthError",0)
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
			self.SetError("self.Lang.AuthError",0);
			return False;


	def _GetDomainNames(self):
		if (self.samrpipe == None): # not connected
			return None
		
		self.domain_name_list = []
		
		self.sam_domains = self.toArray(self.samrpipe.EnumDomains(self.connect_handle, 0, -1))
		for (rid, domain_name) in self.sam_domains:
			self.domain_name_list.append(self.GetLsaString(domain_name))
		
		return self.domain_name_list


	def _SetCurrentDomain(self, domain_index):
		self.domain = self.sam_domains[domain_index]
		self.domain_sid = self.samrpipe.LookupDomain(self.connect_handle, self.domain[1])
		self.domain_handle = self.samrpipe.OpenDomain(self.connect_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, self.domain_sid)
		self.creds.set_domain(self.domain_name_list[domain_index])

	def close(self):
		if (self.samrpipe != None):
			self.samrpipe.Close(self.connect_handle)

	def SetError(self,message,number=-1):
		self.LastErrorStr = message;
		self.LastErrorNumber = number;
		#self.Log.LogError(message);
		self._isLastErrorAvailable=True;
			
	def IHaveError(self):
		return self._isLastErrorAvailable;
	
	@staticmethod
	def toArray((handle, array, num_entries)):
		ret = []
		for x in range(num_entries):
			ret.append((array.entries[x].idx, array.entries[x].name))
		return ret

	@staticmethod
	def GetLsaString(str):
		return str.string
	
	@staticmethod
	def SetLsaString(str):
		lsa_string = lsa.String()
		lsa_string.string = unicode(str)
		lsa_string.length = len(str)
		lsa_string.size = len(str)
		
		return lsa_string
