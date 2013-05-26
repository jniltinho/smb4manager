


from UserModel import UserModel, User


import logging,json


class UserController():
	def __init__(self, username,password):
		self.model = UserModel(username,password);
		self.ChildNodes = [];
		self.users = self.model.GetUserList();
			

	def JsonUsers(self):
		
		total=len(self.users);		

		for user in self.users:
			self.ChildNodes.append({
				'username':user.username
				,'fullname':user.fullname
				,'description':user.description 
				,'rid':user.rid
				,'changepassword':user.must_change_password
				,'cannotchangepassword':user.cannot_change_password
				,'passwordexpires':user.password_never_expires
				,'disable':user.account_disabled
				,'locked':user.account_locked_out
				,'grouplist':user.group_list
				,'profile':user.profile_path
				,'logonscript':user.logon_script
				,'homedir':user.homedir_path
				,'maphomedirdrive':user.map_homedir_drive
				,'type':'user'
			});

		print json.dumps({"Nodos":self.ChildNodes,'total':total}, indent = 2);



        def ListUsers(self):

                total = 0
                for user in self.users:
                        if(user.username not in ['krbtgt','SMB$', 'dns-smb']): 
                              pass
                              total += 1
                              self.ChildNodes.append({'username':user.username 
                                   ,'fullname':user.fullname 
                                   ,'description':user.description 
                                   ,'rid':user.rid
                                   ,'passwordexpires':user.password_never_expires
                                   ,'locked':user.account_locked_out
                              });

                print json.dumps({"Nodos":self.ChildNodes,'total':total}, indent=1);





modelo = UserController('administrator','Teste123456');

modelo.ListUsers()


