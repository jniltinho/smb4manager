# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""


import logging,sys
from samba.param import LoadParm

class AuthBase(object):
	def __init__(self,user,password):
		self.user = user
		self.password = password
		_isLastErrorAvailable=False
		self.lp = LoadParm()
		self.lp.load_default()

		self.logger = logging.getLogger(__name__)
		self.logger.addHandler(logging.StreamHandler(sys.stdout))
		self.logger.setLevel(logging.INFO)
		
	def Autenticate(self):
		pass
	
	def SetError(self,message,number=-1):
		self.LastErrorStr = message
		self.LastErrorNumber = number
		#self.Log.LogError(message)
		self._isLastErrorAvailable=True
			
	def IHaveError(self):
		return self._isLastErrorAvailable
	
