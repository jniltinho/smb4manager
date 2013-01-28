# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from util.smb4_util import SMB4UTIL
from util.ldap_util import LDAPUTIL


@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Hello World'))


@auth.requires_login()
def lista():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    util = LDAPUTIL()
    users = util.getUser(attributes=['sAMAccountName','name'])
    print util.getUser(username='armando')
    return dict(users=users)


@auth.requires_login()
def delete():
    if (request.args): 
         smbtool = SMB4UTIL();
         smbtool.deleteUser(request.args[0])
         response.flash = "User %s DELETEDE" %(request.args[0])
         redirect(URL('index'))
         #return "User %s DELETEDE" %(request.args[0])
    return "Set User for Exclude"



@auth.requires_login()
def add():
    #print "oiiiiiiiiiiiiii"
    #return "Set User for Exclude"
    return dict(message=T('Hello World'))

