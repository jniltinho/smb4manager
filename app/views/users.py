# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort


from app import app
from app.utils import login_required

from app.model.UserModel import UserModel, User

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/')
@login_required
def index():
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    users = model.GetUserList()
    newlist = []
    for user in users:
        if(user.username not in ['krbtgt','SMB$', 'dns-smb']):
              pass
              if (not user.fullname): user.fullname  = user.username
              newlist.append(user)

    return render_template('users/index.html', users=newlist, utils=session['utils'])



@mod.route('/edit/<rid>', methods=["GET", "POST"])
@login_required
def users_edit(rid):
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    user = model.GetUser(int(rid))
    url_redirect = '/users/'
    return_error = 0
    if ((request.method == "POST") and (request.form['submit'] == 'change_pass')):
       message = 'Password Update'
       username = request.form['username']
       password = request.form['password']
       if (session['smb4'][0]['username'].lower() == username.lower()): url_redirect = '/logout/'
       if (not model.SetPassword(username,password)): message=model.LastErrorStr; return_error=1
       data = [{'MESSAGE': message, 'USER': username, 'REDIRECT': url_redirect, 'ERROR': return_error}]
       return jsonify(data=data)


    if ((request.method == "POST") and (request.form['submit'] == 'change_user')):
       message = "User Update"
       user = User(request.form['username'], request.form['fullname'], request.form['description'], request.form['rid'])
       if (not model.UpdateUser(user)): message=model.LastErrorStr; return_error=1
       data = [{'MESSAGE': message, 'USER': request.form['username'], 'REDIRECT': url_redirect, 'ERROR': return_error}]
       return jsonify(data=data)


    return render_template('users/edit.html', utils=session['utils'], user=user)


@mod.route('/add/', methods=["GET", "POST"])
@login_required
def users_add():
    if ((request.method == "POST") and (request.form['submit'] == 'users_add')):

       url_redirect = '/users/'
       message      = "User Created !!"
       return_error = 0
       model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])

       username = request.form['username']
       password = request.form['password']
       mail = request.form['email'] + request.form['domain']
       fullname = request.form['fullname']
       description = request.form['description']

       rid = model.AddUser(username)
       if (rid == False): message=model.LastErrorStr; return_error=1
       data = [{'MESSAGE': message, 'USER': username, 'REDIRECT': url_redirect, 'ERROR': return_error}]

       if (rid):
           user = User(username,fullname,description,rid);
           user.must_change_password = False
           user.password_never_expires = True
           if (not model.UpdateUser(user)): message=model.LastErrorStr; return_error=1
	   if (not model.SetPassword(username,password)): message=model.LastErrorStr; return_error=1 
           data = [{'MESSAGE': message, 'USER': username, 'REDIRECT': url_redirect, 'ERROR': return_error}]

           return jsonify(data=data)

       return jsonify(data=data)
    return render_template('users/add.html', utils=session['utils'])


@mod.route('/del/<username>')
@login_required
def users_del(username):
    user_get = request.args.get('user')
    if(user_get in session['smb4'][0]['username']): return jsonify(message="No Deleted User")
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    del_user = model.DeleteUser(user_get)
    message = "Username: %s deleted with sucess!!" %(user_get)
    if (del_user): return jsonify(message=message)
    return jsonify(message="No Deleted User")




def get_rid_users(username):
    model = UserModel(session['smb4'][0]['username'],session['smb4'][0]['password'])
    users = model.GetUserList()
    newlist = []
    for user in users:
        if (user.username.lower() in [username.lower()] ): return user.rid
        return False


