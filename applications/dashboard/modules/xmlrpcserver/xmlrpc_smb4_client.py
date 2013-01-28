#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Versao 0.21
 
'''
Links:
http://code.activestate.com/recipes/496786-simple-xml-rpc-server-over-https/
http://blogs.blumetech.com/blumetechs-tech-blog/2011/06/python-xmlrpc-server-with-ssl-and-authentication.html
http://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/xmlrpclib/index.html
 
Server:
http://www.pastit.dotcloud.com/194
'''


import xmlrpclib

#Connects to server
#Can only connect over HTTPS with HTTPS server
#Server supports passing username and password

s = xmlrpclib.ServerProxy('https://admin:123456@localhost:8910')

#     Runs various functions on the remote server
print s.div(10,2) 
   

# Print list of available methods
print s.system.listMethods()
