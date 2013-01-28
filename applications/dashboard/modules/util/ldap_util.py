#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## http://dotnetactivedirectory.com/Understanding_LDAP_Active_Directory_User_Object_Properties.html

import ldap
from smb4config import smb4config

domain    = smb4config.SAMBA4['domain']
hostname  = smb4config.SAMBA4['hostname']
user_auth = ('%s@%s' %(smb4config.SAMBA4['admin'], domain))
user_pass = smb4config.SAMBA4['passwd']
 

class LDAPUTIL():
    def _doConnect(self):
        self.l = ldap.initialize("ldap://"+ hostname)
        self.l.protocol_version = ldap.VERSION3
        self.l.set_option(ldap.OPT_REFERRALS, 0)
        self.bind = self.l.simple_bind_s(user_auth, user_pass)
        return self.l

    def _doSearch(self, connect, base, criteria, attributes):
        self.ldp = connect
        self.result = self.ldp.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes,)
        self.results = [entry for dn, entry in self.result if isinstance(entry, dict)]
        self.ldp.unbind()
        return self.results


    def getUser(self, username=False, attributes=['sAMAccountName']):
        self.connect  = self._doConnect()
        self.base     = "dc=%s, dc=%s" %(domain.split('.')[0], domain.split('.')[1])
        if username:
              self.criteria = "(&(objectClass=user)(sAMAccountName=%s))" %(username)
        else:
             self.criteria = "(&(objectClass=user)(userAccountControl:%s:=%u))" %('1.2.840.113556.1.4.803', 512)
        self.attributes = attributes 
        results = self._doSearch(self.connect, self.base, self.criteria, self.attributes)
        return results

