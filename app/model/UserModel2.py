#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# http://msdn.microsoft.com/en-us/library/ms675090%28v=vs.85%29.aspx
# http://www.grotan.com/ldap/python-ldap-samples.html
# http://www.rlmueller.net/Name_Attributes.htm
# http://www.web2ldap.de/
# http://blogs.freebsdish.org/tmclaugh/2010/07/21/finding-a-users-primary-group-in-ad/
# http://www.selfadsi.org/extended-ad/search-user-accounts.htm

import logging, sys, json, ast

import samba, ldb
from samba.dcerpc import samr, security, lsa,srvsvc
from samba import credentials, dsdb, param, version
from samba.auth import system_session
from samba.samdb import SamDB
from samba.param import LoadParm



class UserModel2():
        lp = param.LoadParm()
        lp.load_default()
        WorkGroup = str(lp.get("workgroup"))
        Realm = str(lp.get("realm"))
        creds=None
        LdapConn=None
        samdb=None
        auth_success=False
        _isLastErrorAvailable=False
        LastErrorStr='';
        LastErrorNumber=0;
        RootDSE=''
        DnsDomain=Realm
        schemaNamingContext=''
        server_address='127.0.0.1'
        SambaVersion = version

        def __init__(self,username,password):
               self.creds = credentials.Credentials()
               self.creds.set_username(username)
               self.creds.set_password(password)
               self.creds.set_domain(self.WorkGroup)
               self.creds.set_workstation("")

               self.samdb = SamDB(url='ldap://%s' % self.server_address,session_info=system_session(), credentials=self.creds, lp=self.lp)
               self.samrpipe = samr.samr("ncalrpc:%s"% self.server_address, self.lp, credentials=self.creds)
               self.connect_handle = self.samrpipe.Connect2(None, security.SEC_FLAG_MAXIMUM_ALLOWED)
               self._GetDomainNames()
               self._SetCurrentDomain(0)


        def _SetCurrentDomain(self, domain_index):
               self.domain = self.sam_domains[domain_index]
               self.domain_sid = self.samrpipe.LookupDomain(self.connect_handle, self.domain[1])
               self.domain_handle = self.samrpipe.OpenDomain(self.connect_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, self.domain_sid)
               self.creds.set_domain(self.domain_name_list[domain_index])


        def _GetDomainNames(self):
               if (self.samrpipe == None): return None #not connected
               self.domain_name_list = []
               self.sam_domains = self.toArray(self.samrpipe.EnumDomains(self.connect_handle, 0, -1))
               for (rid, domain_name) in self.sam_domains: self.domain_name_list.append(self.GetLsaString(domain_name))
               return self.domain_name_list


        def GetUser(self, rid=None, user=None):
               all_users = self.ListUsers()
               for user in all_users:
                   if(rid):
                      if user[0]["rid"] == int(rid): return user
                   if(user):
                      if user[0]["samaccountname"] == user: return user


        def ListUsers(self, to_json=False, get_user='All'):

               attrs = ["samaccountname", "mail", "description", "displayname" ]
               lista = []
               rest0 = ''

               expression = ("(&(objectClass=user)(userAccountControl:%s:=%u))"%(ldb.OID_COMPARATOR_AND, dsdb.UF_NORMAL_ACCOUNT))
               if (get_user != 'All'): expression = 'samAccountName=%s' %(get_user)

               res = self.samdb.search(self.samdb.domain_dn(), scope=ldb.SCOPE_SUBTREE,expression=expression, attrs=attrs)

               for i in attrs: rest0 += '"%s": msg.get("%s",idx=0),' %(i,i)
               rids = self.GetRid()
                    
               for msg in res:
                   user = msg.get("samaccountname", idx=0)
                   param = rids[user][0]
                   if (user != 'krbtgt') & (user[:4] != 'dns-'):
                       lista.append( eval('{ "%s": [{ "rid": %s, "account_disabled": %s, %s }] }' %(user, param["rid"], param["account_disabled"], rest0) )) 

               if (to_json): return json.dumps(lista, indent=3)
               simples = []
               for i in range(len(lista)):
                   for user in lista[i]: simples.append(lista[i][user])
               return simples


        def AddUser(self, user, passw, mailaddress=None):
               self.user  = str(user)
               self.passw = str(passw)
               self.mail  = str(mailaddress)
               try:
                   res = self.samdb.newuser(self.user, self.passw, mailaddress=self.mail)
               except Exception,e:
                      print("Failed to add user '%s': %s" %(self.user, e))
                      return False
               return True 



        def GetRid(self, get_user='All'):
               # fetch rid users
               user_rid = ''
               try:
                       self.sam_users = self.toArray(self.samrpipe.EnumDomainUsers(self.domain_handle, 0, 0, -1))

                       for (rid, username) in self.sam_users:
                            user_handle = self.samrpipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid);
                            info = self.samrpipe.QueryUserInfo(user_handle, samr.UserAllInformation)
                            account_disabled = (info.acct_flags & samr.ACB_DISABLED) != 0
                            user_rid += '"%s": [{ "rid": %s, "account_disabled": "%s"}],' %(username.string, rid, account_disabled)
                       return ast.literal_eval(("{ %s }" %user_rid))
               except Exception,e:
                       print(e.message)
                       return False;



        @staticmethod
        def toArray((handle, array, num_entries)):
               ret = []
               for x in range(num_entries): ret.append((array.entries[x].idx, array.entries[x].name))
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



