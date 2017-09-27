# -*- coding: utf-8 -*-

from .proxyhandler import ProxyHandler

from multiprocessing import Process

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import ssl


class ProxyWorker(Process):
    port = 8080

    def __init__(self, port):
        super().__init__()

        self.port = port

    def run(self):
        app = Application([(r'.*', ProxyHandler)])
        server = HTTPServer(app)

        print("Binding port %d" % self.port)
        server.listen(self.port)

        print("Proxy server is up ...")
        loop = IOLoop.instance()
        loop.start()
