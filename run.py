#!flask/bin/python
# -*- coding: utf-8 -*-
## Versao 0.1
## http://blog.perplexedlabs.com/2010/07/01/pythons-tornado-has-swept-me-off-my-feet/

import os, sys
import logging
import argparse
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from rocket import Rocket
from app import app



## Clean .pyc
os.system("find . -type f -iname *.pyc -exec rm  -f {} \;")
os.system("echo 1 > http.log")


def rocket_http(debug=False):
    # Setup logging
    log = logging.getLogger('Rocket')
    log.setLevel(logging.INFO)
    if debug:
       log.addHandler(logging.StreamHandler(sys.stdout))
    else:
       log.addHandler(logging.FileHandler('http.log'))

    # Set the configuration of the web server
    server = Rocket(interfaces=('0.0.0.0', 8010, 'ssl/server.key', 'ssl/server.crt'), method='wsgi', app_info={"wsgi_app": app})
    server.start()



def flask_http():
    from app import app
    port = int(os.environ.get("PORT", 8010))
    app.run(host='0.0.0.0', port=port, debug=True)


def main():
    #----------------------------------------
    # parse arguments
    #----------------------------------------
    parser = argparse.ArgumentParser(description='Start SMB4Manager')
    parser.add_argument('--flask',  action='store_true')
    parser.add_argument('--debug',  action='store_true')
    args = parser.parse_args()

    #----------------------------------------
    # create app files
    #----------------------------------------
    if args.debug:
       rocket_http(debug=args.debug)
       sys.exit(1)

    if args.flask:
       flask_http()
       sys.exit(1)

    rocket_http(debug=False)



if __name__ == "__main__":
       main()

