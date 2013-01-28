# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import os

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

