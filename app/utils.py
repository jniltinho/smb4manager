
## Flask
import os
from functools import wraps
from flask import url_for, redirect, flash, request, session

from model.auth.AuthSMB4 import AuthSMB4


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
          if 'username' in session:
               return f(*args, **kwargs)
          else:
               flash("A login is required to see the page!")
               return redirect(url_for('default.login', next=request.path))
    return wrapper


def isAuthenticate(username, password):
     base = AuthSMB4(username,password)
     return base.Autenticate()



def getiUtils():
    if (session['username'] and session['password']):
       from app.model.base import BaseModel
       model = BaseModel(session['username'],session['password'])
       return [{ 'domain':model.GetDomain(),'login_user':session['username'].title() }]
    return  [{ 'domain':'notfound.local','login_user':'Nologin' }]

