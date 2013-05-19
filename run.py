#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Versao 0.1

import os
import argparse



def gunicorn_http(debug=False):
    logfile = '--log-file=http.log'
    if debug : logfile = ''
    os.system("find . -type f -iname *.pyc -exec rm  -f {} \;")
    os.system("echo 1 > http.log")
    os.system("source env/bin/activate; gunicorn -w 2 --bind 0.0.0.0:8010 app:app --keyfile=ssl/server.key --certfile=ssl/server.crt " + logfile )


def flask_http():
    from app import app
    port = int(os.environ.get("PORT", 8010))
    app.run(host='0.0.0.0', port=port)


def main():
        #----------------------------------------
        # parse arguments
        #----------------------------------------
        parser = argparse.ArgumentParser(description='Start SMB4Manager')
        parser.add_argument('--flask', action='store_true')
        parser.add_argument('--desenv', action='store_true')
        parser.add_argument('--prod', action='store_true')
        parser.add_argument('--debug', action='store_true')
        args = parser.parse_args()

        #----------------------------------------
        # create app files
        #----------------------------------------
        if args.prod:
            gunicorn_http(debug=args.debug)

        if args.desenv:
            gunicorn_http(debug=args.debug)

        if args.flask:
            flask_http()




if __name__ == "__main__":
        main()

