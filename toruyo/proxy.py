# -*- coding: utf-8 -*-

from .proxyhandler import ProxyHandler

from multiprocessing import Process

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application


class ProxyWorker(Process):
    def __init__(self, port, address='0.0.0.0', dump_root='./'', patterns=[]):
        super().__init__()

        self.port = port
        self.address = address
        self.dump_root = dump_root
        self.patterns = patterns

    def run(self):
        app = Application([(r'.*', ProxyHandler)])
        server = HTTPServer(app)

        for p in self.patterns:
            print("  pattern: " + str(p))

        print("Binding port %d" % self.port)
        server.bind(self.port, address=self.address)
        server.start(0)

        print("Proxy server is up ...")
        loop = IOLoop.instance()
        loop.start()
