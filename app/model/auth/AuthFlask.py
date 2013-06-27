
## Flask
import os,functools
from flask import url_for, redirect, flash, request, session


from AuthSMB4 import AuthSMB4


class AuthFlask():

        def login_required(self,method):
            @functools.wraps(method)
            def wrapper(*args, **kwargs):
                if 'username' in session:
                    return method(*args, **kwargs)
                else:
                    flash("A login is required to see the page!")
                    return redirect(url_for('default.login'))
            return wrapper


        def isAuthenticate(self, username, password):
            base = AuthSMB4(username,password)
            return base.Autenticate()



        def getiUtils(self):
            if (session['username'] and session['password']):
               from app.model.base import BaseModel
               model = BaseModel(session['username'],session['password'])
               return [{ 'domain':model.GetDomain(),'login_user':session['username'].title() }]
            return  [{ 'domain':'notfound.local','login_user':'Nologin' }]

