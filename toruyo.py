#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from toruyo.proxy import ProxyWorker

import sys
import os.path
from multiprocessing import Process

from tornado.options import define, options
from tornado.options import parse_command_line, parse_config_file

define("bind", default="0.0.0.0", help="ip address that bind to", type=str)
define("port", default=8000, help="port number that listen to", type=int)
define("dump_root", default=8000, help="root dir's path for dumping", type=str)
define("patterns", default=[], help="list of matching patterns", type=list)
define("config", default="toruyo.conf", help="config file", type=str)

if __name__ == "__main__":
    parse_command_line()
    if options.config:
        parse_config_file(options.config)
    parse_command_line()

    print("*** Starting cache proxy worker ***")
    pw = ProxyWorker(
        port=options.port,
        address=options.bind,
        dump_root=options.dump_root,
        patterns=options.patterns)
    pw.start()

    pw.join()
