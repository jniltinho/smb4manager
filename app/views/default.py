# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import Blueprint, render_template, session, redirect, url_for, request, flash, g, jsonify, abort

from app import app
from users import get_rid_users

from app.utils import login_required, isAuthenticate, getiUtils

mod = Blueprint('default', __name__)


@mod.route('/')
@login_required
def index():
    return render_template('default/index.html', utils=session['utils'])



# === User login methods ===
@mod.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form['username']
        password = request.form['password']
        if isAuthenticate(username, password):
            session.permanent = True
            session['username'] = username
            session['password'] = password
            session['utils']    = getiUtils()
            session['smb4']     = [{'username':username, 'password':password, 'ipaddr':request.remote_addr}]
            session['smb4'][0]['rid'] = get_rid_users(username)

            return redirect(request.values.get('next') or url_for('default.index'))
        else:
            flash("Username doesn't exist or incorrect password")
    return render_template('default/login.html')


@mod.route('/logout/', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    return redirect(request.referrer or url_for('default.index'))



@mod.route('/dashboard/')
@login_required
def dashboard():
    return render_template('default/dashboard.html')

