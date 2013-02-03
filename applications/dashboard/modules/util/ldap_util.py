#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## http://dotnetactivedirectory.com/Understanding_LDAP_Active_Directory_User_Object_Properties.html


from base import *



class LDAPUTIL():

    lp = param.LoadParm()
    lp.load_default()

    def __init__(self, smb4config):
        self.config    = smb4config
        self.domain    = self.config.get('samba_config', 'domain')
        self.hostname  = self.config.get('samba_config', 'hostname')
        self.admin     = self.config.get('samba_config', 'admin')
        self.username = ('%s@%s' %(self.admin, self.domain))
        self.password = self.config.get('samba_config', 'passwd')


    def _connect(self):
        try:
            creds = credentials.Credentials()
            creds.set_username(self.username)
            creds.set_password(self.password)
            creds.set_domain("")
            creds.set_workstation("")
            self.conn = samba.Ldb("ldap://"+ self.hostname,lp=self.lp,credentials=creds)
        except Exception,e:
                raise
        return True;


    def _doSearch(self, base, criteria, attributes):
        if self._connect():
           dn = ldb.Dn(self.conn, base)
           self.result = self.conn.search(dn,scope=ldb.SCOPE_SUBTREE,expression=criteria, attrs=attributes)
           for msg in self.result: print  msg['sAMAccountName']
           return self.result
        return False


    def getUser(self, username=False, attributes=['sAMAccountName']):
        dn = self.domain.split('.')
        self.BaseDn     = "CN=Users,DC=%s,DC=%s" %(dn[0], dn[1])
        if username:
           self.criteria = "(&(objectClass=user)(sAMAccountName=%s))" %(username)
        else:
           self.criteria = "(&(objectClass=user)(userAccountControl:%s:=%u))" %('1.2.840.113556.1.4.803', 512)
           self.attributes = attributes 
           results = self._doSearch(self.BaseDn, self.criteria, self.attributes)
           return results
