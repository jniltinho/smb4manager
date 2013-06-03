#!flask/bin/python
# -*- coding: utf-8 -*-
## Versao 0.1

import os, sys
import argparse


def gunicorn_http(debug=False):
    logfile = '--log-file=http.log'
    if debug : logfile = ''
    os.system("find . -type f -iname *.pyc -exec rm  -f {} \;")
    os.system("echo 1 > http.log")
    os.system("flask/bin/gunicorn -w 2 --bind 0.0.0.0:8010 app:app --keyfile=ssl/server.key --certfile=ssl/server.crt " + logfile )
    #os.system("flask/bin/gunicorn -w 2 --bind unix:/tmp/gunicorn_flask.sock app:app --keyfile=ssl/server.key --certfile=ssl/server.crt " + logfile )



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
    parser.add_argument('--desenv', action='store_true')
    parser.add_argument('--debug',  action='store_true')
    args = parser.parse_args()

    #----------------------------------------
    # create app files
    #----------------------------------------
    if args.debug:
       gunicorn_http(debug=args.debug)
       sys.exit(1)

    if args.desenv:
       gunicorn_http(debug=args.debug)
       sys.exit(1)

    if args.flask:
       flask_http()
       sys.exit(1)

    gunicorn_http()



if __name__ == "__main__":
       main()

