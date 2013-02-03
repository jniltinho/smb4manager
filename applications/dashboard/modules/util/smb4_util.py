

import os,commands


class SMB4UTIL():
  def __init__(self,smb4config):
      self.config  = smb4config
      self.cmd_smb = self.config.get('samba_config', 'smbtool')


  def _erros(self,msg=False):
      if 'successfully' in msg:
          return ['SUCCESS', 'Account created successfully']

      if 'Failed' in msg:
          if 'complexity' in msg: return ['FAILED', 'Password not complexity']
          if 'already' in msg: return ['FAILED', 'Account already in use']

      return (True,msg)


  def getUser(self):
      cmd_result = commands.getoutput(self.cmd_smb + ' user list')
      return cmd_result.split()



  def addUser(self,username=False, password=False, mail=False, givenname=False, surname=False):
      if not username: return Response("unknown_username")
      if not password: return Response("unknown_password")
      cmd_add = ("%s user add %s %s --mail-address=%s --given-name='%s' --surname='%s'") %(self.cmd_smb, username, password, mail, givenname, surname)
      ##print cmd_add
      cmd_result = commands.getoutput(cmd_add)
      cmd_result = self._erros(cmd_result)
      return cmd_result



  def deleteUser(self,username=False):
      if not username: return Response("error_set_username")
      cmd = ('%s user delete %s') %(self.cmd_smb, username)
      cmd_result = commands.getoutput(cmd)
      return cmd_result.split()


