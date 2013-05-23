# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	DATABASE_URI = 'sqlite:///application.db'
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "MINHACHAVESECRETA"
	CSRF_ENABLED = True
	USERS = {'administrator':'123456', 'linuxpro':'linuxpro12'}



class SMBConfig(Config):
	DEBUG = True
	NOME = "NEW SMB4Manager Flask APP"

