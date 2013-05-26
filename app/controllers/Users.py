# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import url_for, jsonify, redirect, request, render_template, send_from_directory, flash, session

from app import app

from app.model.auth.AuthFlask import AuthFlask
auth = AuthFlask()

from app.model.UserModel import UserModel, User



@app.route('/users/')
@auth.login_required
def users():
    model = UserModel(session['username'],session['password'])
    users = model.GetUserList()
    utils = _getDomain()
    newuserlist = []
    for user in users:
        if(user.username not in ['krbtgt','SMB$', 'dns-smb']):
              pass
              if (not user.fullname): user.fullname  = user.username
              newuserlist.append(user)


    return render_template('users.html', users=newuserlist, utils=utils)



def _getDomain():
    if (session['username'] and session['password']):
        from app.model.base import BaseModel
        model = BaseModel(session['username'],session['password'])
        ChildNodes = [{ 'domain':model.GetDomain(),'login_user':session['username'].title() }]
        return ChildNodes
    return 'domain.notfound'


