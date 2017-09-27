#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from toruyo import proxy

import sys
from multiprocessing import Process

if __name__ == "__main__":
    port = 37893
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print("Starting cache proxy on port %d" % port)
#    proxy.run_proxy(port)
    proxy_process = Process(target=proxy.run_proxy, args=[port])
    proxy_process.start()
    print("Started.")
