#!flask/bin/python
# -*- coding: utf-8 -*-
## Versao 0.1
## http://blog.perplexedlabs.com/2010/07/01/pythons-tornado-has-swept-me-off-my-feet/

import os, sys
import logging
import argparse
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


from app import app

## Clean .pyc
os.system("find . -type f -iname *.pyc -exec rm  -f {} \;")
os.system("echo 1 > http.log")


def flask_http(debug=False, ssl=False):
    if (ssl):
        from OpenSSL import SSL
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file('ssl/server.key')
        context.use_certificate_file('ssl/server.crt')
        app.run(host='0.0.0.0', port=8010, debug=debug, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=8010, debug=debug)


def main():
    #----------------------------------------
    # parse arguments
    #----------------------------------------
    parser = argparse.ArgumentParser(description='Start SMB4Manager')
    parser.add_argument('--flask',  action='store_true')
    parser.add_argument('--ssl',    action='store_true')
    parser.add_argument('--debug',  action='store_true')
    args = parser.parse_args()

    #----------------------------------------
    # create app files
    #----------------------------------------
    if args.flask:
       flask_http(debug=args.debug, ssl=args.ssl)
       sys.exit(1)

    flask_http(debug=args.debug, ssl=args.ssl)



if __name__ == "__main__":
       main()

