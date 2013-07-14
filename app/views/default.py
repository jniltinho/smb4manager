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


@mod.route('/data.json', methods=["GET", "POST"])
@login_required
def data_json():
    data = {"total":28,"rows":[
	{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,"attr1":"Large","itemid":"EST-1"},
	{"productid":"K9-DL-01","productname":"Dalmation","unitcost":12.00,"status":"P","listprice":18.50,"attr1":"Spotted Adult Female","itemid":"EST-10"},
	{"productid":"RP-SN-01","productname":"Rattlesnake","unitcost":12.00,"status":"P","listprice":38.50,"attr1":"Venomless","itemid":"EST-11"},
	{"productid":"RP-SN-01","productname":"Rattlesnake","unitcost":12.00,"status":"P","listprice":26.50,"attr1":"Rattleless","itemid":"EST-12"},
	{"productid":"RP-LI-02","productname":"Iguana","unitcost":12.00,"status":"P","listprice":35.50,"attr1":"Green Adult","itemid":"EST-13"},
	{"productid":"FL-DSH-01","productname":"Manx","unitcost":12.00,"status":"P","listprice":158.50,"attr1":"Tailless","itemid":"EST-14"},
	{"productid":"FL-DSH-01","productname":"Manx","unitcost":12.00,"status":"P","listprice":83.50,"attr1":"With tail","itemid":"EST-15"},
	{"productid":"FL-DLH-02","productname":"Persian","unitcost":12.00,"status":"P","listprice":23.50,"attr1":"Adult Female","itemid":"EST-16"},
	{"productid":"FL-DLH-02","productname":"Persian","unitcost":12.00,"status":"P","listprice":89.50,"attr1":"Adult Male","itemid":"EST-17"},
	{"productid":"AV-CB-01","productname":"Amazon Parrot","unitcost":92.00,"status":"P","listprice":63.50,"attr1":"Adult Male","itemid":"EST-18"}
        ]} 

    return jsonify(data)
