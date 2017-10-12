# -*- coding: utf-8 -*-

import os
from datetime import datetime
import fcntl
from urllib.parse import urlparse
from queue import Queue, Empty
from threading import Thread, Event


class Dumper(object):

    def __init__(self, num=1, path='./'):
        self.queue = Queue()
        self.stopping = Event()
        self.threads = []
        self.TIMEOUT = 60
        self.root_path = os.path.abspath(path)

        for i in range(num):
            t = Thread(target=self.__work, args=(i, self.queue))
            self.threads.append(t)

    def __work(self, n, q):
        # n - Worker ID
        # q - Queue from which to receive data
        while not self.stopping.is_set():
            try:
                tpl = q.get(True, self.TIMEOUT)
                req = tpl[0]   # request
                res = tpl[1]   # response
                uri = urlparse(req.uri)

                tmp_path = os.path.join(self.root_path, uri.hostname)
                tmp_path += uri.path
                (filedirs, filename) = os.path.split(tmp_path)
                filename = 'index.html' if filename == '' else filename
                dump_path = os.path.join(filedirs, filename)

                # create dirs if not exists
                if not os.path.isdir(filedirs):
                    os.makedirs(filedirs)

                # dump files
                with open(dump_path, 'wb') as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    f.write(res.body)
                    f.flush()
                    fcntl.flock(f, fcntl.LOCK_UN)

            except Empty:
                continue

    def request(self, http_req, http_res):
        self.queue.put((http_req, http_res))

    def run(self):
        for t in self.threads:
            t.start()

    def join(self):
        self.queue.join()
        self.stopping.set()
