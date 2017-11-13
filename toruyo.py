#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from src.proxy import Proxy

import os
from tornado.options import define, options
from tornado.options import parse_command_line, parse_config_file

from os.path import abspath

define("bind", default="0.0.0.0", help="ip address that bind to", type=str)
define("port", default=8000, help="port number that listen to", type=int)
define("dump_root", default="./", help="root dir's path to dump", type=str)
define("config", default="./proxy.conf", help="config file", type=str)
define("patterns", default="./patterns.json", help="rule pattern file",
       type=str)
define("debug", default=False, help="run in debug mode", type=bool)
define("num_processes", default=0, help="number of sub-processes(0:auto)",
       type=int)
define("num_dumpers", default=5, help="number of dumping threads", type=int)


def main():
    parse_command_line()
    if options.config and os.path.exists(options.config):
        parse_config_file(options.config)
    parse_command_line()

    print("*** Starting cache proxy worker ***")
    proxy = Proxy(
        port=options.port,
        address=options.bind,
        dump_root=abspath(options.dump_root),
        patterns=abspath(options.patterns),
        debug=options.debug,
        num_processes=options.num_processes,
        num_dumpers=options.num_dumpers)
    proxy.start()

    proxy.join()


if __name__ == "__main__":
    main()
