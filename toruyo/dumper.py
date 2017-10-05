# -*- coding: utf-8 -*-

from threading import Thread, Event
from queue import Queue, Empty


class Dumper(object):

    def __init__(self, num):
        self.queue = Queue()
        self.stopping = Event()
        self.threads = []
        self.TIMEOUT = 60

        for i in range(num):
            t = Thread(target=self.__work, args=(i, self.queue))
            self.threads.append(t)

    def __work(self, n, q):
        # n - Worker ID
        # q - Queue from which to receive data
        while not self.stopping.is_set():
            try:
                data = q.get(True, self.TIMEOUT)
                print('worker ' + str(n) + ' got ' + str(data))
            except Empty:
                continue

    def put_request(self, args):
        self.queue.put(args)

    def run(self):
        for t in self.threads:
            t.start()

    def join(self):
        self.queue.join()
        self.stopping.set()
