# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, functools
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)

#Configuration of application, see configuration.py, choose one and uncomment.
#app.config.from_object('configuration.ProductionConfig')
app.config.from_object('app.configuration.DevelopmentConfig')
#app.config.from_object('configuration.TestingConfig')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return method(*args, **kwargs)
        else:
            flash("A login is required to see the page!")
            return redirect(url_for('login'))
    return wrapper


#from app import controllers.Login

from controllers import Login, Index, Users
