#!/bin/env python
# -*- coding: utf-8 -*-

from handler import ProxyHandler

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


if __name__ == "__main__":
    port = 37893
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print("Starting cache proxy on port %d" % port)
    run_proxy(port)
    #run_ssl_proxy(8888)
