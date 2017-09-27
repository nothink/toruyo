# -*- coding: utf-8 -*-

from .proxyhandler import ProxyHandler

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import ssl


def run_proxy(port):
    app = tornado.web.Application([(r'.*', ProxyHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)

    print("Server is up ...")
    tornado.ioloop.IOLoop.instance().start()
