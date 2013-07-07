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


import base64
import time
from base2 import *


class UserModel2(BaseModel):
        def __init__(self,username,password):
                BaseModel.__init__(self,username,password)


        def newuser(self):
                if self.isAuthenticate():
                   #return self.samdb.domain_dn()
                   self.domain_dn = self.samdb.domain_dn()
                   res = self.samdb.search(self.domain_dn, scope=ldb.SCOPE_SUBTREE,expression=("(&(objectClass=user)(userAccountControl:%s:=%u))"
                                                               %(ldb.OID_COMPARATOR_AND, dsdb.UF_NORMAL_ACCOUNT)), attrs=["samaccountname", "mail", "description"])
                   for msg in res:
                       print("%s %s %s") %(msg.get("samaccountname", idx=0), msg.get("mail", idx=0), msg.get("description", idx=0))
