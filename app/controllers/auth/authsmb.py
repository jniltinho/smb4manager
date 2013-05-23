# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, functools
from flask import url_for, redirect, flash, request, session

#getip = request.remote_addr


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return method(*args, **kwargs)
        else:
            flash("A login is required to see the page!")
            return redirect(url_for('login'))
    return wrapper

