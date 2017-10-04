# -*- coding: utf-8 -*-

from .dumper import Dumper

import sys
import os
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import tornado.httputil


class ProxyHandler(tornado.web.RequestHandler):
    ''' Proxy Handler Class '''
    logger = None

    @tornado.web.asynchronous
    def get(self):
        ''' GET request event handling　(Transparently). '''
        try:
            # Remove harmful 'Proxy-Connection' header.
            if 'Proxy-Connection' in self.request.headers:
                del self.request.headers['Proxy-Connection']
            req = tornado.httpclient.HTTPRequest(
                url=self.request.uri,
                method=self.request.method,
                body=self.request.body if self.request.body else None,
                headers=self.request.headers,
                follow_redirects=False,
                allow_nonstandard_methods=True)
            client = tornado.httpclient.AsyncHTTPClient()
            client.fetch(req, self.handle_response, raise_error=False)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                self.handle_response(e.response)
            else:
                self.set_status(500)
                self.write('500 Internal server error:\n' + str(e))
                self.finish()

    def handle_response(self, response):
        '''  Handling all response datas... and dump. '''
        if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
            self.set_status(500)
            self.write('500 Internal server error:\n' + str(response.error))
        else:
            self.set_status(response.code, response.reason)
            self._headers = tornado.httputil.HTTPHeaders()

            for header_k, v in response.headers.get_all():
                EXCLUDE_HEADERS = (
                    'Content-Length',
                    'Transfer-Encoding',
                    'Content-Encoding',
                    'Connection',
                )
                if header_k not in EXCLUDE_HEADERS:
                    self.add_header(header_k, v)

            if response.body:
                # Dump urls.
                dt = Dumper(self.request.uri)
                dt.start()
                # Write threw.
                self.write(response.body)
        self.finish()

    post = get
