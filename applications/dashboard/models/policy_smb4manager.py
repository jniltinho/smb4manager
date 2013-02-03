response.title = T('SMB4Manager')





def no_show_users(useraccount):
    no_users = ['Guest', 'krbtgt']
    if (useraccount in no_users) or (useraccount[:4] == 'dns-'): return True
	
