# -*- coding: utf-8 -*-

from threading import Thread

class Dumper(Thread):
    url = ''

    def __init__(self, url):
        super().__init__()

        self.url = url

    def run(self):
        print(self.url)
