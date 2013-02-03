#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## http://dotnetactivedirectory.com/Understanding_LDAP_Active_Directory_User_Object_Properties.html

import ldap

 

class LDAPUTIL():
  def __init__(self,smb4config):
      self.config    = smb4config
      self.domain    = self.config.get('samba_config', 'domain')
      self.hostname  = self.config.get('samba_config', 'hostname')
      self.admin     = self.config.get('samba_config', 'admin')
      self.user_auth = ('%s@%s' %(self.admin, self.domain))
      self.user_pass = self.config.get('samba_config', 'passwd')


  def _doConnect(self):
      self.l = ldap.initialize("ldap://"+ self.hostname)
      self.l.protocol_version = ldap.VERSION3
      self.l.set_option(ldap.OPT_REFERRALS, 0)
      self.bind = self.l.simple_bind_s(self.user_auth, self.user_pass)
      return self.l

  def _doSearch(self, connect, base, criteria, attributes):
      self.ldp = connect
      self.result = self.ldp.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes,)
      self.results = [entry for dn, entry in self.result if isinstance(entry, dict)]
      self.ldp.unbind()
      return self.results


  def getUser(self, username=False, attributes=['sAMAccountName']):
      self.connect  = self._doConnect()
      dn = self.domain.split('.')
      self.base     = "dc=%s, dc=%s" %(dn[0], dn[1])
      if username:
         self.criteria = "(&(objectClass=user)(sAMAccountName=%s))" %(username)
      else:
         self.criteria = "(&(objectClass=user)(userAccountControl:%s:=%u))" %('1.2.840.113556.1.4.803', 512)
         self.attributes = attributes 
         results = self._doSearch(self.connect, self.base, self.criteria, self.attributes)
         return results


