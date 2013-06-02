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
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    users = model.GetUserList()
    newlist = []
    for user in users:
        if(user.username not in ['krbtgt','SMB$', 'dns-smb']):
              pass
              if (not user.fullname): user.fullname  = user.username
              newlist.append(user)


    return render_template('users.html', users=newlist, utils=session['utils'])



@app.route('/users/edit/<rid>', methods=["GET", "POST"])
@auth.login_required
def users_edit(rid):
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    user = model.GetUser(int(rid))
    return render_template('users_edit.html', utils=session['utils'], user=user)



@app.route('/users/add/', methods=["GET", "POST"])
@auth.login_required
def users_add():
    if request.method == "POST":
       model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])

       username = request.form['sAMAccountName']
       password = request.form['userPassword']
       mail = request.form['sAMAccountName'] + request.form['domain']
       fullname = "%s %s" %(request.form['givenName'], request.form['surname'])
       description = "SMB4Manager Created User"

       rid = model.AddUser(username)
       if (rid):
           user = User(username,fullname,description,rid);
           user.must_change_password = False
           user.password_never_expires = True
           model.UpdateUser(user)
           model.SetPassword(username, password)
           message = "Username: %s Fullname: %s Created" %(username, fullname)
           return jsonify(message=message)

       return jsonify(addform="Username Not Create")
    return render_template('users_add.html', utils=session['utils'])


@app.route('/users/del/<username>')
@auth.login_required
def users_del(username):
    user_get = request.args.get('user')
    if(user_get in session['smb4'][0]['username']): return jsonify(message="No Deleted User")
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    del_user = model.DeleteUser(user_get)
    message = "Username: %s deleted with sucess!!" %(user_get)
    if (del_user): return jsonify(message=message)
    return jsonify(message="No Deleted User")

