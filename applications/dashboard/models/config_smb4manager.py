# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()


## Logging
import logging
logger = logging.getLogger("web2py.app.dashboard")
#logger.setLevel(logging.DEBUG)



# Using ConfigParser to read config in ini
# Allows us to prevent sensitive data in our repo
import os
from os.path import join
from ConfigParser import SafeConfigParser


def get_config():
    config = SafeConfigParser()
    config.read(join(request.folder, 'smb4config.ini'))
    return config



db = DAL('sqlite://dbauth.sqlite')

from gluon.tools import Auth
auth = Auth(db)


## configure auth policy
#auth.settings.formstyle = 'divs'
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.controller = 'account'
auth.settings.login_url=URL('account','login')

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)



### Configure LDAP AUTH
### http://www.web2pyslices.com/slice/show/1493/active-directory-ldap-with-allowed-groupsUTH
#auth.define_tables(username=True)
#auth.settings.create_user_groups=False
# all we need is login
#auth.settings.actions_disabled=['register','change_password','request_reset_password','retrieve_username','profile']
# you don't have to remember me
#auth.settings.remember_me_form = False
# ldap authentication and not save password on web2py
#from gluon.contrib.login_methods.ldap_auth import ldap_auth
#auth.settings.login_methods = [ldap_auth(mode='ad',server='127.0.0.1',base_dn='dc=domain,dc=local')]

