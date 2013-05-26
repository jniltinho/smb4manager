# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, functools
from flask import Flask

app = Flask(__name__)


app.config.from_object('app.configuration.SMBConfig')



## Init App
from controllers import Main, Login, Users

