#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Versao 0.30

'''
Links:
http://code.activestate.com/recipes/496786-simple-xml-rpc-server-over-https/
http://blogs.blumetech.com/blumetechs-tech-blog/2011/06/python-xmlrpc-server-with-ssl-and-authentication.html
http://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/xmlrpclib/index.html
'''

import ast, signal, socket
import ssl, fcntl, SocketServer
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

signal.signal(signal.SIGINT, signal.SIG_DFL)

import smb4_util

from ConfigParser import ConfigParser
config = ConfigParser()
config.read('server.conf')

# Configure below
LISTEN_HOST = config.get('SERVER', 'host')
LISTEN_PORT = int(config.get('SERVER', 'port'))

KEYFILE  = config.get('SERVER', 'keyfile')
CERTFILE = config.get('SERVER', 'certfile')

#Easiest way to create the key file pair was to use OpenSSL -- http://openssl.org/ Windows binaries are available
#You can create a self-signed certificate easily "openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout privatekey.pem"
#for more information --  http://docs.python.org/library/ssl.html#ssl-certificates

userPassDict = ast.literal_eval(config.get('AUTH', 'users'))
   
class SimpleXMLRPCServerTLS(SimpleXMLRPCServer):
    def __init__(self, addr, requestHandler=SimpleXMLRPCRequestHandler,
                 logRequests=True, allow_none=False, encoding=None, bind_and_activate=True):
        """Overriding __init__ method of the SimpleXMLRPCServer

        The method is an exact copy, except the TCPServer __init__
        call, which is rewritten using TLS
        """
        self.logRequests = logRequests

        SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding)

        """This is the modified part. Original code was:

            SocketServer.TCPServer.__init__(self, addr, requestHandler, bind_and_activate)

        which executed:

            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
                BaseServer.__init__(self, server_address, RequestHandlerClass)
                self.socket = socket.socket(self.address_family,
                                            self.socket_type)
                if bind_and_activate:
                    self.server_bind()
                    self.server_activate()

        """
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            '''
            Request Handler that verifies username and password passed to
            XML RPC server in HTTP URL sent by client.
            '''
            # this is the method we must override
            def parse_request(self):
                # first, call the original implementation which returns
                # True if all OK so far
                if SimpleXMLRPCRequestHandler.parse_request(self):
                    # next we authenticate
                    if self.authenticate(self.headers):
                        return True
                    else:
                        # if authentication fails, tell the client
                        self.send_error(401, 'Authentication failed')
                return False
           
            def authenticate(self, headers):
                from base64 import b64decode
                #    Confirm that Authorization header is set to Basic
                (basic, _, encoded) = headers.get('Authorization').partition(' ')
                assert basic == 'Basic', 'Only basic authentication supported'
               
                #    Encoded portion of the header is a string
                #    Need to convert to bytestring
                encodedByteString = encoded.encode()
                #    Decode Base64 byte String to a decoded Byte String
                decodedBytes = b64decode(encodedByteString)
                #    Convert from byte string to a regular String
                decodedString = decodedBytes.decode()
                #    Get the username and password from the string
                (username, _, password) = decodedString.partition(':')
                #    Check that username and password match internal global dictionary
                if username in userPassDict:
                    if userPassDict[username] == password:
                        return True
                return False
       
        #    Override the normal socket methods with an SSL socket
        SocketServer.BaseServer.__init__(self, addr, VerifyingRequestHandler)
        self.socket = ssl.wrap_socket(
            socket.socket(self.address_family, self.socket_type),
            server_side=True,
            keyfile=KEYFILE,
            certfile=CERTFILE,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23,
            )
        if bind_and_activate:
            self.server_bind()
            self.server_activate()

        """End of modified part"""

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/api','/RPC2', '/webserver')

def executeRpcServer():
    # Create server
    server = SimpleXMLRPCServerTLS((LISTEN_HOST, LISTEN_PORT), requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_multicall_functions()

    server.register_instance(smb4_util.SMB4UTIL())
    sa = server.socket.getsockname()
    print "Starting XMLRPCServer HTTPS on", sa[0], "port", sa[1]
    server.serve_forever()


if __name__ == '__main__':  
    executeRpcServer()
