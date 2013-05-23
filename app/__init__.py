# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, functools
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)


app.config.from_object('app.configuration.SMBConfig')


lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'



#from app import controllers.Login

from controllers import Login, Index, Users

print app.config['NOME']
