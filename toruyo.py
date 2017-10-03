#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from toruyo.proxy import ProxyWorker

import sys
import os.path
from multiprocessing import Process

from tornado.options import define, options
import tornado.options

define("port", default=8000, help="port number", type=int)
define("config", default="toruyo.conf", help="config file", type=str)

if __name__ == "__main__":
    tornado.options.parse_config_file(os.path.abspath(options.config))
    tornado.options.parse_command_line()

    print(options.port)

    print("Starting cache proxy worker")
    pw = ProxyWorker(port=options.port)
    pw.start()

    pw.join()
