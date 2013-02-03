import logging

from adsbrowser.lib.base import *
from adsbrowser.model.UserModel import UserModel;

log = logging.getLogger(__name__)

class UserController(BaseController):

	def __init__(self):
		#super(BaseController,self).__init__()
		BaseController.__init__(self)
		#response.write('__init__');
		if self._check_session():
			self.model = UserModel(session['username'],session['password']);
		
		
	def EnableAccount(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
		try:
			dn = request.params.get("dn","")
			username = request.params.get("username","")
			enable = request.params.get("enable","yes").strip();
			
			
			if(self.model.isAuthenticate()):
				if(enable == "yes"):
					enable=True
				else:
					enable=False
					
				if(not self.model.EnableAccount(dn,username,enable)):
					raise Exception(self.model.LastErrorStr);

			else:
				raise Exception(self.model.LastErrorStr);
		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		#return json.dumps(self.successOK)
		return json.dumps({'success': True,'enable':enable})


		
		
	def ForcePasswordChangeAtNextLogin(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
			
		try:
			dn = request.params.get("dn","")
			username = request.params.get("username","")
			if(self.model.isAuthenticate()):
				if(not self.model.ForcePasswordChangeAtNextLogin(dn,username)):
					raise Exception(self.model.LastErrorStr);

		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		return json.dumps(self.successOK)



	def SetPassword(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
			
		try:
			dn = request.params.get("dn","")
			username = request.params.get("username","")
			password = request.params.get("password",samba.generate_random_password(7,15))
			
			
			#response.write(password);
			if(self.model.isAuthenticate()):
				if(not self.model.SetPassword(dn,username,password)):
					raise Exception(self.model.LastErrorStr);
			
			UnlockUserAccount = request.params.get("UnlockUserAccount",False)
			if(UnlockUserAccount != False):
				if(not self.model.EnableAccount(dn,username,True)):
					raise Exception(self.model.LastErrorStr);
			
			ForcePasswordChange = request.params.get("ForcePasswordChange",False)
			if(ForcePasswordChange != False):
				if(not self.model.ForcePasswordChangeAtNextLogin(dn,username)):
					raise Exception(self.model.LastErrorStr);
			

		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		return json.dumps(self.successOK)


	def SetExpiry(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
			
		try:
			dn = request.params.get("dn","")
			username = request.params.get("username","")
			no_expiry_req = request.params.get("expiry",'no')
			
			if(no_expiry_req != 'no'):
				expiry = True;
			else:
				expiry = False;
				
			
			days = int(request.params.get("days",15))

			if(self.model.isAuthenticate()):
				if(not self.model.SetExpiry(dn,username,days,expiry)):
					raise Exception(self.model.LastErrorStr);

		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		#response.write(samba.unix2nttime(299044800))
		#response.write(samba.nttime2string(119435184000000000))
		return json.dumps(self.successOK)


