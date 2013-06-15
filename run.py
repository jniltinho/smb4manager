#!flask/bin/python
# -*- coding: utf-8 -*-
## Versao 0.1
## http://blog.perplexedlabs.com/2010/07/01/pythons-tornado-has-swept-me-off-my-feet/

import os, sys
import argparse
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


## Clean .pyc
os.system("find . -type f -iname *.pyc -exec rm  -f {} \;")
os.system("echo 1 > http.log")


def tornado_http(ssl=False):
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from app import app
    if ssl:
       http_server = HTTPServer(WSGIContainer(app),ssl_options={"certfile": os.path.join("ssl/", "server.crt"),"keyfile": os.path.join("ssl/", "server.key"),})
    else:
       http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8010, address='0.0.0.0')
    IOLoop.instance().start()


def gunicorn_http(debug=False):
    if debug :
       os.system("flask/bin/gunicorn -w 2 --bind 0.0.0.0:8010 app:app")
    else:
       os.system("flask/bin/gunicorn -w 2 --bind 0.0.0.0:8010 app:app --log-file=http.log")


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
    parser.add_argument('--ssl',  action='store_true')
    parser.add_argument('--tornado',  action='store_true')
    args = parser.parse_args()

    #----------------------------------------
    # create app files
    #----------------------------------------
    if args.debug:
       gunicorn_http(debug=args.debug)
       sys.exit(1)

    if args.tornado or args.ssl:
       tornado_http(ssl=args.ssl)
       sys.exit(1)

    if args.flask:
       flask_http()
       sys.exit(1)

    tornado_http(ssl=True)



if __name__ == "__main__":
       main()

