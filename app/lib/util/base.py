"""The base Controller API

Provides the BaseController class for subclassing.
"""
import os, sys, StringIO
lib_samba = ['/opt/samba4/lib/python2.7/site-packages', '/usr/local/samba/lib/python2.7/site-packages']

for i in lib_samba:
    if (os.path.exists(i)): sys.path.append(i) 



import samba
import ldb
from samba.dcerpc import samr, security, lsa
from samba import credentials
from samba import param
from samba.auth import system_session
from samba.samdb import SamDB


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
