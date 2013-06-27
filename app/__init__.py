# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from datetime import timedelta
import os, functools
from flask import Flask, session, g, render_template, send_from_directory

app = Flask(__name__)

app.config.from_object('app.configuration')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


## Init App
from views import default, users

app.register_blueprint(default.mod)
app.register_blueprint(users.mod)


from app import utils
