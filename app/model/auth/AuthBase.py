# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os, functools
from flask import url_for, redirect, flash, request, session

#getip = request.remote_addr



class AuthBase(object):


       def login_required(self,method):
           @functools.wraps(method)
           def wrapper(*args, **kwargs):
               if 'username' in session:
                   return method(*args, **kwargs)
               else:
                   flash("A login is required to see the page!")
                   return redirect(url_for('login'))
           return wrapper

	
