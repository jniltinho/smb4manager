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
    newuserlist = []
    for user in users:
        if(user.username not in ['krbtgt','SMB$', 'dns-smb']):
              pass
              if (not user.fullname): user.fullname  = user.username
              newuserlist.append(user)


    return render_template('users.html', users=newuserlist, utils=session['utils'])



@app.route('/users/add/', methods=["GET", "POST"])
@auth.login_required
def users_add():
    if request.method == "POST":
       addform =  [{'givenName': request.form['givenName'], 'surname': request.form['surname'], 
         'sAMAccountName': request.form['sAMAccountName'], 
         'mail': request.form['mail'], 'userPassword': request.form['userPassword'] 
        }]  
       return jsonify( { 'addform': addform[0] } )


