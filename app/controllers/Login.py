# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import url_for, redirect, request, render_template, send_from_directory, flash, session

from app import app

from app.model.auth.AuthFlask import AuthFlask
auth = AuthFlask()


# === User login methods ===

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form['username']
        password = request.form['password']
        if auth.isAuthenticate(username, password):
            session.permanent = True
            session['username'] = username
            session['password'] = password
            session['utils']    = auth.getiUtils()

            session['smb4']     = [{'username':username, 'password':password, 'ipaddr':request.remote_addr}]

            return redirect(url_for('index'))
        else:
            flash("Username doesn't exist or incorrect password")
    return render_template('login.html')


@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



