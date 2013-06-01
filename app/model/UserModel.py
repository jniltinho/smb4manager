


import base64
import time
from base import *
from GroupModel import GroupModel
from samba.net import Net


class UserModel(BaseModel):

	def __init__(self,username,password):
		BaseModel.__init__(self,username,password)
		self.user_list = []
		if self.isAuthenticate():
			self.net = Net(self.creds,self.lp,server=self.server_address)
			self.LoadUserList();

	def AddUser(self,username):
		if self.isAuthenticate():
			try:
				#Creates the new user on the server using default values for everything. Only the username is taken into account here.
				(user_handle, rid) = self.samrpipe.CreateUser(self.domain_handle, self.SetLsaString(username), security.SEC_FLAG_MAXIMUM_ALLOWED)		
				user = self.GetUser(rid)
				#response.write('ok');
				#user.rid = rid #update the user's RID
				#if user.group_list == []: #The user must be part of a group. If the user is not part of any groups, the user is actually part of the "None" group! 
				#	user.group_list = new_user.group_list #use the default values assigned to the user when it was created on the server, which is probably "None"
				self.UpdateUser(user)
			except Exception,e:
				self.SetError(e.args[1],e.args[0])
				#Printer(e);
				#response.write(str(dir(e)));
				return False;
			return rid;
		else:
			return False;

	def Exists(self, rid):
		""" Checks if a certain User (identified by its RID) exists in the
		Database
		
		Keyword arguments:
		rid -- The RID of the User to check
		
		Returns:
		Boolean indicating if the User exists or not
		
		TODO Handle Exception
		
		"""
		exists = False
		
		try:
			rid=int(rid)
			self.samrpipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid)
			exists = True
		except RuntimeError:
			pass
		
		return exists
		
	def LoadUserList(self,AllUserInformation=False):
		# fetch users
		try:
			self.sam_users = self.toArray(self.samrpipe.EnumDomainUsers(self.domain_handle, 0, 0, -1))
			for (rid, username) in self.sam_users:
				#FIXME optimize
				user = self.GetUser(rid)
				self.user_list.append(user)
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True;

	def GetUserList(self):
		return self.user_list

	def GetUser(self, rid, user = None):
		try:
			rid = int(rid);
			user_handle = self.samrpipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, rid);
			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserAllInformation);
			user = self.QueryInfoToUser(info, user);
			user.group_list = self.GetUserGroups(rid);
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return user

	def QueryInfoToUser(self, query_info, user = None):
		try:
			if (user == None):
				user = User(self.GetLsaString(query_info.account_name), 
							self.GetLsaString(query_info.full_name), 
							self.GetLsaString(query_info.description), 
							query_info.rid)
			else:
				user.username = self.GetLsaString(query_info.account_name)
				user.full_name = self.GetLsaString(query_info.full_name)
				user.description = self.GetLsaString(query_info.description)
				user.rid = query_info.rid
			
			user.must_change_password = (query_info.acct_flags & samr.ACB_PW_EXPIRED) != 0
			user.password_never_expires = (query_info.acct_flags & samr.ACB_PWNOEXP) != 0
			user.account_disabled = (query_info.acct_flags & samr.ACB_DISABLED) != 0
			user.account_locked_out = (query_info.acct_flags & samr.ACB_AUTOLOCK) != 0
			#cannot_change_password doesn't get set in a flag, it's a little different
			user.profile_path = self.GetLsaString(query_info.profile_path)
			user.logon_script = self.GetLsaString(query_info.logon_script)
			user.homedir_path = self.GetLsaString(query_info.home_directory)
			
			drive = self.GetLsaString(query_info.home_drive)
			if (len(drive) == 2):
				#user.map_homedir_drive = ord(drive[0]) - ord('A')
				user.map_homedir_drive = drive
			else:
				user.map_homedir_drive = -1
		except Exception,e:
			self.SetError(e.message,0)
			return False;
			
		return user


	def SetPassword(self,username,password):
		try:
			
			self.net.set_password(username,self.domain_name_list[0],password)
			#self.net.set_password(username,self.domain_name_list[0],password,self.creds)
			#net.set_password(username,'SAMDOM',password,self.creds)
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True;

	def DeleteUser(self,username):
		try:
			self.net.delete_user(username)		
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True;		
		


	def EnableAccount(self,rid,username,enable=True):
		try:
			user = self.GetUser(rid);
			if isinstance(user,User):
				user.account_disabled = not enable;
				self.UpdateUser(user);
			else:
				raise Exception(self.LastErrorStr);
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True

	def ForcePasswordChangeAtNextLogin(self,rid,username,MustChange=True):
		try:
			user = self.GetUser(rid);
			if isinstance(user,User):
				user.must_change_password = MustChange;
				self.UpdateUser(user);
			else:
				raise Exception(self.LastErrorStr);
		except Exception,e:
			self.SetError(e.message,0)
			return False;
		return True

	def UpdateUser(self, user):
		if not self.isAuthenticate():
			self.SetError("self.Lang.NotAuth",0)
			return False;

		try:
			user_handle = self.samrpipe.OpenUser(self.domain_handle, security.SEC_FLAG_MAXIMUM_ALLOWED, user.rid)

			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserNameInformation)
			info.account_name = self.SetLsaString(user.username)
			info.full_name = self.SetLsaString(user.fullname)
			self.samrpipe.SetUserInfo(user_handle, samr.UserNameInformation, info)
			
			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserAdminCommentInformation)
			info.description = self.SetLsaString(user.description)
			self.samrpipe.SetUserInfo(user_handle, samr.UserAdminCommentInformation, info)
			
			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserControlInformation)
			#user.must_change_password = True;
			if (user.must_change_password):
				info.acct_flags |= samr.ACB_PW_EXPIRED
			else:
				info.acct_flags &= ~samr.ACB_PW_EXPIRED

			if (user.password_never_expires):
				info.acct_flags |= samr.ACB_PWNOEXP
			else:
				info.acct_flags &= ~samr.ACB_PWNOEXP
				
			if (user.account_disabled):
				info.acct_flags |= samr.ACB_DISABLED
			else:
				info.acct_flags &= ~samr.ACB_DISABLED

			if (user.account_locked_out):
				info.acct_flags |= samr.ACB_AUTOLOCK
			else:
				info.acct_flags &= ~samr.ACB_AUTOLOCK
			self.samrpipe.SetUserInfo(user_handle, samr.UserControlInformation, info)

			#User cannot change password is updated in the security function
			#self.UpdateUserSecurity(user_handle, user)

			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserProfileInformation)
			info.profile_path = self.SetLsaString(user.profile_path)
			self.samrpipe.SetUserInfo(user_handle, samr.UserProfileInformation, info)
			
			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserScriptInformation)
			info.logon_script = self.SetLsaString(user.logon_script)
			self.samrpipe.SetUserInfo(user_handle, samr.UserScriptInformation, info)

			info = self.samrpipe.QueryUserInfo(user_handle, samr.UserHomeInformation)
			info.home_directory = self.SetLsaString(user.homedir_path)
			
			
			#if (user.map_homedir_drive.strip() == -1):
			#	info.home_drive = self.SetLsaString("")
			#else:
				#info.home_drive = self.SetLsaString(chr(user.map_homedir_drive + ord('A')) + ":")
			info.home_drive = self.SetLsaString(user.map_homedir_drive)
			self.samrpipe.SetUserInfo(user_handle, samr.UserHomeInformation, info)
		except Exception,e:
			self.SetError(e.message,0)
			return False;

		return True;
		
	def UpdateUserSecurity(self, user_handle, user):
		"""Updates the access mask for 'user'.
		
		returns nothing"""
		secinfo = self.samrpipe.QuerySecurity(user_handle, security.SECINFO_DACL)
		sid = str(self.samrpipe.RidToSid(self.domain_handle, user.rid))
		#f = open("info.txt", 'wb')
		#import pickle
		#f.write(str(dir(secinfo)))
		#pickle.dump(secinfo, f) 
		#f.close()
		#this is for readability, we could just do secinfo.sd.dacl.aces[i].trustee if we wanted
		security_descriptor = secinfo.sd
		DACL = security_descriptor.dacl
		ace_list = DACL.aces
		

		
		ace = None
			
		for item in ace_list:
			if str(item.trustee) == sid:
				ace = item
				break
			
		if ace == None:
			#print "unable to fetch security info for", user.username, "because none exists."
			return user
		
		if user.cannot_change_password:
			ace_list[0].access_mask &= ~samr.SAMR_USER_ACCESS_CHANGE_PASSWORD
			ace.access_mask &= ~samr.SAMR_USER_ACCESS_CHANGE_PASSWORD
		else:
			ace_list[0].access_mask |= samr.SAMR_USER_ACCESS_CHANGE_PASSWORD
			ace.access_mask |= samr.SAMR_USER_ACCESS_CHANGE_PASSWORD
			
		self.samrpipe.SetSecurity(user_handle, security.SECINFO_DACL, secinfo)
		return

	def GetUserGroups(self,rid):
		groups = GroupModel(self.username,self.password);
		GroupList = groups.GetUserGroups(rid);
		return GroupList;

class User:

	def __init__(self, username, fullname, description, rid):
		self.username = username
		self.fullname = fullname
		self.description = description
		self.rid = int(rid)
		
		self.password = ""
		self.must_change_password = True
		self.cannot_change_password = False
		self.password_never_expires = False
		self.account_disabled = False
		self.account_locked_out = False
		self.group_list = []
		self.profile_path = ""
		self.logon_script = ""
		self.homedir_path = ""
		self.map_homedir_drive = ""

class Printer:

	def __init__ (self, PrintableClass):
		for name in dir(PrintableClass):
			value = getattr(PrintableClass,name)
			if  '_' not in str(name).join(str(value)):
				print('  .%s: %r' % (name, value))

  
