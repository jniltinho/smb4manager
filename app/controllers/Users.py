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
#USERS = {'administrator':'123456'}


@app.route('/users/')
@login_required
def users():
    return render_template('users.html')


