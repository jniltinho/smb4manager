import logging
from adsbrowser.lib.base import *

from samba.dsdb import (UF_NORMAL_ACCOUNT, UF_ACCOUNTDISABLE,
	UF_WORKSTATION_TRUST_ACCOUNT, UF_SERVER_TRUST_ACCOUNT,
	UF_PARTIAL_SECRETS_ACCOUNT, UF_TEMP_DUPLICATE_ACCOUNT,
	UF_PASSWD_NOTREQD, ATYPE_NORMAL_ACCOUNT,
	GTYPE_SECURITY_BUILTIN_LOCAL_GROUP, GTYPE_SECURITY_DOMAIN_LOCAL_GROUP,
	GTYPE_SECURITY_GLOBAL_GROUP, GTYPE_SECURITY_UNIVERSAL_GROUP,
	GTYPE_DISTRIBUTION_DOMAIN_LOCAL_GROUP, GTYPE_DISTRIBUTION_GLOBAL_GROUP,
	GTYPE_DISTRIBUTION_UNIVERSAL_GROUP,
	ATYPE_SECURITY_GLOBAL_GROUP, ATYPE_SECURITY_UNIVERSAL_GROUP,
	ATYPE_SECURITY_LOCAL_GROUP, ATYPE_DISTRIBUTION_GLOBAL_GROUP,
	ATYPE_DISTRIBUTION_UNIVERSAL_GROUP, ATYPE_DISTRIBUTION_LOCAL_GROUP,
	ATYPE_WORKSTATION_TRUST , SYSTEM_FLAG_DOMAIN_DISALLOW_RENAME)



import StringIO
log = logging.getLogger(__name__)

class BrowserController(BaseController):
	def __init__(self):
		BaseController.__init__(self);
		self.ChildNodes = []; 
		self.ParentNode = {"Nodos":self.ChildNodes};

	def index(self):
		response.headers['Content-type'] = 'text/html; charset=utf-8'
		if self._check_session():
			c.title = "Active Directory Browser 0.1"
			c.auth = True
			c.DnsDomain = session['DnsDomain'];
			c.RootDSE = session['RootDSE'];
			
		return render('/index.html')

	def getGridElements(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);

		try:
			node = request.params.get("node",session['RootDSE'])
			self.BaseDn = node 
			#node = "OU=Domain Controllers,DC=samdom,DC=example,DC=com"
			if self._connect():
				dn = ldb.Dn(self.conn, node);
				#conn = ldb.Ldb("ldap://127.0.0.1")
				#req.write(str(dir(ldb.Ldb)));
				#res = conn.search(node,scope=ldb.SCOPE_ONELEVEL,expression="(&(name=*)(!(showinadvancedviewonly=True)))",attrs=['dn','name','displayname','samaccounttype','samaccountname', "description",'objectclass','objectCategory','groupType','useraccountcontrol','systemflags','iscriticalsystemobject'])
				res = self.conn.search(dn,scope=ldb.SCOPE_ONELEVEL,expression="(&(name=*)(!(showinadvancedviewonly=True)))")
				#response.write(str(dn));
		except ldb.LdbError, (num, msg):
				return json.dumps({'success': False, 'msg': msg,'num':num}) 			
		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0}) 


		for msg in res:
			#req.write(str(msg.dn)+"<br>")
			#req.write(str(msg['isCriticalSystemObject'])+"<br>")
			name= msg['name'][0];
			icon = '';
			typeText= '-';
			is_container = False;
			is_ou = False;
			ObjectName = str(msg.dn).split(',')[0];
			disable = False
			groupType=0;
			is_group=False;
				
			samaccounttype= 0;
			if('sAMAccountType' in msg):
				samaccounttype= int(msg['sAMAccountType'][0]);

				
			if('sAMAccountName' in msg):
				samaccountname= msg['sAMAccountName'][0];
			else:
				samaccountname= '';

				
			objectClass= msg['objectclass'];

				
			#if('groupType' in msg):
			#	if (int(msg['groupType'][0]) == GTYPE_SECURITY_GLOBAL_GROUP):
			#		typeText= 'Grupo de Seguridad Global';
			#	elif (int(msg['groupType'][0]) == GTYPE_SECURITY_DOMAIN_LOCAL_GROUP):
			#		typeText= 'Grupo de Seguridad Local';
			#	elif (int(msg['groupType'][0]) == GTYPE_SECURITY_BUILTIN_LOCAL_GROUP):
			#		typeText= 'Grupo Integrado';
			#	elif (int(msg['groupType'][0]) == GTYPE_SECURITY_UNIVERSAL_GROUP):
			#		typeText= 'Grupo de Seguridad Universal';
			#		
			#else:
			#	typeText= '-';
			if('groupType' in msg):
				groupType=int(msg['groupType'][0]);
				typeText = self._getGroupType(groupType);
				icon = 'group-icon';
				is_group = True;
				
			if(typeText=='-'):
				obj = {"typeText":typeText,"icon":icon};
				self._getAccType(samaccounttype,obj);
				typeText = obj['typeText'];			
				icon = obj["icon"];

			objectClass= msg['objectclass'];
			objectClassList = [];
			PossSuperiorsList = [];
			for i in objectClass:
				objectClassList.append(i);
				PossSuperiorsList.extend(self._getPossSuperiors(i));

			PossSuperiorsList = list(set(PossSuperiorsList));
			
				
			if("organizationalUnit" in objectClass):
				icon = 'folderou-icon';
				typeText= 'Unidad Organizativa';
				is_container = True;
				is_ou = True;
			
			if("container" in objectClass):
				typeText= 'Contenedor';
				is_container = True;
				
			if("builtinDomain" in objectClass):
				typeText= 'builtinDomain';
				samaccounttype = 'builtinDomain';
				is_container = True;
			
			draggable = True;
			if("systemflags" in msg):
				if (int(msg['systemflags'][0]) & SYSTEM_FLAG_DOMAIN_DISALLOW_RENAME):
					draggable=False;

			if("isCriticalSystemObject" in msg):
				if (msg['isCriticalSystemObject'][0] == 'TRUE'):
					draggable=False;
			
			description = '-'
			if("description" in msg):
				description=msg['description'][0]
				
			if("userAccountControl" in msg):
				if (int(msg['userAccountControl'][0]) & 0x2):
					disable = True;
					icon = 'dusuario';
			systemPossSuperiors={};
			if("systemPossSuperiors" in msg):
				for i in msg['systemPossSuperiors']:
					systemPossSuperiors[i]= msg['systemPossSuperiors'][i];
			
			self.ChildNodes.append({
				'name':name
				,'samaccountname':samaccountname
				,'type':samaccounttype
				,'groupType':groupType
				,'is_group':is_group
				,'typeText':typeText
				,'description':description
				,'id':str(msg.dn)
				,'icon':icon
				,'is_container':is_container
				,'is_ou':is_ou
				,'ObjectName':ObjectName
				,'oldParentDn':str(msg.dn.parent())
				,'draggable':draggable
				,'disable':disable
				,'systemPossSuperiors':PossSuperiorsList
				,'objectClass':objectClassList
			});
		return json.dumps({"Nodos":self.ChildNodes,"BaseDn":self.BaseDn});



	def getTreeNodes(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);
		is_ou = False;
		is_container = False;
		try:
			node = request.params.get("node",session['RootDSE'])
			#node = "OU=Domain Controllers,DC=samdom,DC=example,DC=com"
			if self._connect():
				dn = ldb.Dn(self.conn, node);
				#conn = ldb.Ldb("ldap://127.0.0.1")
				#req.write(str(dir(ldb.Ldb)));
				#res = conn.search(node,scope=ldb.SCOPE_ONELEVEL,expression="(&(name=*)(!(showinadvancedviewonly=True)))",attrs=['dn','name','displayname','samaccounttype','samaccountname', "description",'objectclass','objectCategory','groupType','useraccountcontrol','systemflags','iscriticalsystemobject'])
				res = self.conn.search(dn,scope=ldb.SCOPE_ONELEVEL,expression="(|(showInAdvancedViewOnly=FALSE)(ou=*)(&(objectclass=container)(showInAdvancedViewOnly=FALSE)))")
				#response.write(str(dn));
		except ldb.LdbError, (num, msg):
				return json.dumps({'success': False, 'msg': msg,'num':num}) 			
		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0}) 


		for msg in res:
			name= msg['name'][0];
			icon = '';
			typeText='';
			ObjectName = str(msg.dn).split(',')[0];

				
			draggable = True;
			if("systemflags" in msg):
				if (int(msg['systemflags'][0]) & SYSTEM_FLAG_DOMAIN_DISALLOW_RENAME):
					draggable=False;

			if("isCriticalSystemObject" in msg):
				if (msg['isCriticalSystemObject'][0] == 'TRUE'):
					draggable=False;
			samaccounttype= 0;
			if('sAMAccountType' in msg):
				samaccounttype= int(msg['samaccounttype'][0]);


			objectClass= msg['objectclass'];

			objectClass= msg['objectclass'];
			objectClassList = [];
			PossSuperiorsList = [];
			for i in objectClass:
				objectClassList.append(i);
				PossSuperiorsList.extend(self._getPossSuperiors(i));

			PossSuperiorsList = list(set(PossSuperiorsList));
			
			
			if("organizationalUnit" in objectClass):
				icon = 'folderou-icon';
				is_container = True;
				is_ou = True;
			
			if("container" in objectClass):
				typeText= 'Contenedor';
				is_container = True;
				
			if("builtinDomain" in objectClass):
				samaccounttype = 'builtinDomain';
				is_container = True;
			
			self.ChildNodes.append({
				'text':name
				,'id':str(msg.dn)
				,'iconCls':icon
				,'ObjectName':ObjectName
				,'oldParentDn':str(msg.dn.parent())
				,'draggable':draggable
				,'type':samaccounttype
				,'is_ou':is_ou
				,'is_container':is_container
				,'systemPossSuperiors':PossSuperiorsList
				,'objectClass':objectClassList				
			});
		return json.dumps(self.ChildNodes);


	def move(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);

		try:
			old_dn = request.params.get("dn","")
			new_dn = request.params.get("newdn","")
			if self._connect():
				old_dn = ldb.Dn(self.conn, old_dn);
				new_dn = ldb.Dn(self.conn, new_dn);
				self.conn.rename(old_dn,new_dn);
		except ldb.LdbError, (num, msg):
				return json.dumps({'success': False, 'msg': msg,'num':num}) 			
		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		return json.dumps(self.successOK)
		

	def delete(self):
		if not self._check_session():
			return json.dumps(self.AuthErr);

		try:

			if self._connect():
				dn = request.params.get("dn","")
				dn = ldb.Dn(self.conn, dn);
				self.conn.delete(dn);

		except ldb.LdbError, (num, msg):
				return json.dumps({'success': False, 'msg': msg,'num':num}) 			
		except Exception,e:
				return json.dumps({'success': False, 'msg': e.message,'num':0})
		return json.dumps(self.successOK)


	def _getGroupType(self,GTYPE):
		if(GTYPE == GTYPE_SECURITY_BUILTIN_LOCAL_GROUP):
			return "Grupo de Seguridad - Dominio local";
		elif(GTYPE == GTYPE_SECURITY_GLOBAL_GROUP):
			return "Grupo de Seguridad - Global";
		elif(GTYPE == GTYPE_SECURITY_DOMAIN_LOCAL_GROUP):
			return "Grupo de Seguridad - Dominio local";
		elif(GTYPE == GTYPE_SECURITY_UNIVERSAL_GROUP):
			return "Grupo de Seguridad - Universal";
		elif(GTYPE == GTYPE_DISTRIBUTION_GLOBAL_GROUP):
			return "Grupo de Distribuci&oacute;n - Global";
		elif(GTYPE == GTYPE_DISTRIBUTION_DOMAIN_LOCAL_GROUP):
			return "Grupo de Distribuci&oacute;n - Dominio local";
		elif(GTYPE == GTYPE_DISTRIBUTION_UNIVERSAL_GROUP):
			return "Grupo de Distribuci&oacute;n - Universal";
		else:
			return "-";
		


	def _getAccType(self,samaccounttype,dic):
#		/* Account flags for "sAMAccountType" */
#		ATYPE_NORMAL_ACCOUNT	 =		0x30000000 /* 805306368 */
#		ATYPE_WORKSTATION_TRUST =			0x30000001 /* 805306369 */
#		ATYPE_INTERDOMAIN_TRUST	=		0x30000002 /* 805306370 */
#		ATYPE_SECURITY_GLOBAL_GROUP =		0x10000000 /* 268435456 */
#		ATYPE_SECURITY_LOCAL_GROUP	=	0x20000000 /* 536870912 */
#		ATYPE_SECURITY_UNIVERSAL_GROUP =		ATYPE_SECURITY_GLOBAL_GROUP
#		ATYPE_DISTRIBUTION_GLOBAL_GROUP	=	0x10000001 /* 268435457 */
#		ATYPE_DISTRIBUTION_LOCAL_GROUP	=	0x20000001 /* 536870913 */
#		ATYPE_DISTRIBUTION_UNIVERSAL_GROUP =	ATYPE_DISTRIBUTION_GLOBAL_GROUP
#
#		ATYPE_ACCOUNT	=	ATYPE_NORMAL_ACCOUNT		/* 0x30000000 805306368 */
#		ATYPE_GLOBAL_GROUP =	ATYPE_SECURITY_GLOBAL_GROUP	/* 0x10000000 268435456 */
#		ATYPE_LOCAL_GROUP =	ATYPE_SECURITY_LOCAL_GROUP	/* 0x20000000 536870912 */

		if(samaccounttype == int(ATYPE_NORMAL_ACCOUNT)):
			dic["typeText"]=  'Usuario';
			dic["icon"] = 'usuario';
		elif (samaccounttype == int(ATYPE_WORKSTATION_TRUST)):
			dic["typeText"]=  'Equipo';
			dic["icon"] = 'pc-icon';
		#elif (samaccounttype == int(ATYPE_SECURITY_LOCAL_GROUP)):
		#	dic["typeText"]=  'Grupo Local';
		#	dic["icon"] = 'group-icon';
		#elif (samaccounttype == int(ATYPE_SECURITY_GLOBAL_GROUP)):
		#	dic["typeText"]=  'Grupo Global';	
		#	dic["icon"] = 'groups-icon';

	def _getPossSuperiors(self,objectClass):
		class_attrs = [
						"possSuperiors", 
						"systemPossSuperiors",
					]
					

		res = self.conn.search(expression="lDAPDisplayName=%s"%objectClass, 
									 base=session['schemaNamingContext'], scope=ldb.SCOPE_SUBTREE,attrs=class_attrs)
		list = [];
		for msg in res:
			for a in msg:
				if(type(msg[a]) != ldb.Dn):
					i = 0;
					for k in msg[a]:
						#print "\t"+a+" "+str(msg[a].get(i))
						list.append(msg[a].get(i));
						i=i+1;
		return list;
