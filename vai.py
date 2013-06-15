#!flask/bin/python
# -*- coding: utf-8 -*-
## Versao 0.1

import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

#http_server = HTTPServer(WSGIContainer(app))
http_server = HTTPServer(WSGIContainer(app),ssl_options={"certfile": "ssl/server.crt", "keyfile": "ssl/server.key"),})
http_server.listen(8010)
IOLoop.instance().start()
