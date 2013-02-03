from base import BaseController
import ldb

from samba.dsdb import (UF_NORMAL_ACCOUNT, UF_ACCOUNTDISABLE,
        UF_WORKSTATION_TRUST_ACCOUNT, UF_SERVER_TRUST_ACCOUNT,
        UF_PARTIAL_SECRETS_ACCOUNT, UF_TEMP_DUPLICATE_ACCOUNT,
        UF_PASSWD_NOTREQD, ATYPE_NORMAL_ACCOUNT,
        GTYPE_SECURITY_BUILTIN_LOCAL_GROUP, GTYPE_SECURITY_DOMAIN_LOCAL_GROUP,
        GTYPE_SECURITY_GLOBAL_GROUP, GTYPE_SECURITY_UNIVERSAL_GROUP,
        GTYPE_DISTRIBUTION_DOMAIN_LOCAL_GROUP, GTYPE_DISTRIBUTION_GLOBAL_GROUP,
        GTYPE_DISTRIBUTION_UNIVERSAL_GROUP,
        ATYPE_SECURITY_GLOBAL_GROUP, ATYPE_SECURITY_UNIVERSAL_GROUP,
        ATYPE_SECURITY_LOCAL_GROUP, ATYPE_DISTRIBUTION_GLOBAL_GROUP,
        ATYPE_DISTRIBUTION_UNIVERSAL_GROUP, ATYPE_DISTRIBUTION_LOCAL_GROUP,
        ATYPE_WORKSTATION_TRUST , SYSTEM_FLAG_DOMAIN_DISALLOW_RENAME)



import StringIO



class BrowserController(BaseController):

        def __init__(self):
            self.ChildNodes = [];
            self.ParentNode = {"Nodos":self.ChildNodes};


        def getGridElements(self):
            node = "CN=Users,DC=criare,DC=local"
            self.BaseDn = node
            if self._connect():
               dn = ldb.Dn(self.conn, node);
               print self.conn
               criteria = "(&(objectClass=user)(sAMAccountName=*))"
               res = self.conn.search(dn,scope=ldb.SCOPE_SUBTREE,expression=criteria, attrs=['sAMAccountName'])
               for msg in res:
                   print  msg['sAMAccountName']











casa = BrowserController()
casa.getGridElements()

#conn = ldb.Ldb("ldap://127.0.0.1")
#req.write(str(dir(ldb.Ldb)));
#res = conn.search(node,scope=ldb.SCOPE_ONELEVEL,expression="(&(name=*)(!(showinadvancedviewonly=True)))",attrs=['dn','name','displayname','samaccounttype','samaccountname', "description",'objectclass','objectCategory','groupType','useraccountcontrol','systemflags','iscriticalsystemobject'])
#res = self.conn.search(dn,scope=ldb.SCOPE_ONELEVEL,expression="(&(name=*)(!(showinadvancedviewonly=True)))")

#response.write(str(dn));


#for msg in res:
#name = msg['name'][0];

