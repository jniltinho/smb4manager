# user management
#
# Copyright Jelmer Vernooij 2010 <jelmer@samba.org>
# Copyright Theresa Halloran 2011 <theresahalloran@gmail.com>
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


import base64, time

import samba
import ldb
import logging, sys
from samba.dcerpc import samr, security, lsa,srvsvc
from samba import credentials, dsdb, param
from samba.auth import system_session
from samba.samdb import SamDB
from samba import version
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


        def ListUsers(self):
               self.domain_dn = self.samdb.domain_dn()
               res = self.samdb.search(self.domain_dn, scope=ldb.SCOPE_SUBTREE,expression=("(&(objectClass=user)(userAccountControl:%s:=%u))"
                                                               %(ldb.OID_COMPARATOR_AND, dsdb.UF_NORMAL_ACCOUNT)), attrs=["samaccountname", "mail", "description"])
               for msg in res:
                   print("%s %s %s") %(msg.get("samaccountname", idx=0), msg.get("mail", idx=0), msg.get("description", idx=0))



        def AddUser(self, user, passw, mailaddress=None):
               self.user  = str(user)
               self.passw = str(passw)
               self.mail  = str(mailaddress)
               try:
                   res = self.samdb.newuser(self.user, self.passw, mailaddress=self.mail)
               except Exception,e:
                      print("Failed to add user '%s': %s" %(username, e))
                      return False
               return True 


