# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def login():
    return dict(form=auth.login(next=URL('default','index')))

@auth.requires_login()
def logout(): auth.logout(next=URL(r=request,c='default',f='index'))
	
