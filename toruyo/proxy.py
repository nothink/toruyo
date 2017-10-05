
# -*- coding: utf-8 -*-

from .handler import ProxyHandler
#from .dumper.channel import DumpChannel
from .dumper import Dumper

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

        self.dumper = Dumper(5)

    def run(self):
        self.dumper.run()
        app = Application(
            [(r'.*', ProxyHandler, dict(dumper=self.dumper))],
            debug=self.debug)
        server = HTTPServer(app)

        print("Binding port %d" % self.port)
        server.bind(self.port, address=self.address)
        server.start(1)

        print("Proxy server is up ...")
        loop = IOLoop.instance()
        loop.start()
