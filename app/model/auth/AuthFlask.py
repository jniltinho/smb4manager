
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
                    return redirect(url_for('login'))
            return wrapper


        def isAuthenticate(self, username, password):
            base = AuthSMB4(username,password)
            return base.Autenticate()

