# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, json
from flask import url_for, redirect, request, render_template, send_from_directory, flash, session

from app import app
from auth.authsmb import *


@app.route('/')
@login_required
def index():
    return render_template('index.html')


# ====================
