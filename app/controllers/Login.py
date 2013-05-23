# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import url_for, redirect, request, render_template, send_from_directory, flash, g, session
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)
from app import app, lm
from app.forms import ExampleForm, LoginForm

from auth.authsmb import *

USERS = {'administrator':'123456'}



# === User login methods ===

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Username doesn't exist or incorrect password")
    return render_template('login.html')


@app.route('/logout/', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# ====================
