#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from toruyo.proxy import ProxyWorker

import sys
from multiprocessing import Process

if __name__ == "__main__":
    port = 37893
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print("Starting cache proxy worker")
    pw = ProxyWorker(port=port)
    pw.start()

    pw.join()
