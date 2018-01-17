# -*- coding: utf-8 -*-

from .handler import ProxyHandler
from .dumper import Dumper

from multiprocessing import Process

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application


class Proxy(Process):
    def __init__(self, port, address='0.0.0.0',
                 dump_root='./',
                 patterns=[], debug=False,
                 num_processes=0, num_dumpers=5):
        super().__init__()

        self.port = port
        self.address = address
        self.patterns = patterns
        self.debug = debug
        self.num_processes = num_processes

        self.dumper = Dumper(num=num_dumpers, path=dump_root)

    def run(self):
        self.dumper.run()
        app = Application(
            [(r'.*', ProxyHandler, dict(dumper=self.dumper))],
            debug=self.debug)
        server = HTTPServer(app)

        print("Binding port %d" % self.port)
        server.bind(self.port, address=self.address)
        server.start(self.num_processes)

        print("Proxy server is up ...")
        loop = IOLoop.instance()
        loop.start()

    def join(self, timeout=None):
        super().join(timeout)
        self.dumper.join()
