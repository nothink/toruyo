
# -*- coding: utf-8 -*-

from .handler import ProxyHandler

from multiprocessing import Process

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application


class Proxy(Process):
    def __init__(self, port, address='0.0.0.0', dump_root='./',
                 patterns=[], debug=False):
        super().__init__()

        self.port = port
        self.address = address
        self.dump_root = dump_root
        self.patterns = patterns
        self.debug = debug

    def run(self):
        app = Application([(r'.*', ProxyHandler)], debug=self.debug)
        server = HTTPServer(app)

        print("Binding port %d" % self.port)
        server.bind(self.port, address=self.address)
        server.start(1)

        print("Proxy server is up ...")
        loop = IOLoop.instance()
        loop.start()
