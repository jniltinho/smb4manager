
## Flask
import os,functools
from flask import url_for, redirect, flash, request, session


from AuthBase import AuthBase


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
            base = AuthBase(username,password)
            return base.Autenticate()

