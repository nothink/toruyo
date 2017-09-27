# -*- coding: utf-8 -*-

from .dumper import Dumper

import sys
import os
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import ssl


class ProxyHandler(tornado.web.RequestHandler):
    ''' Proxy Handler Class '''
    @tornado.web.asynchronous
    def get(self):
        ''' GET request event handling '''
        return self.represent()

    @tornado.web.asynchronous
    def post(self):
        ''' POST request event handling '''
        return self.represent()

    def represent(self):
        ''' Transparent proxy event handling '''
        def get_response(response):
            if response.error and not isinstance(response.error, tornado.httpclient.HTTPError):
                self.set_status(500)
                self.write('500 error:\n' + str(response.error))
                self.finish()
            else:
                self.set_status(response.code)
                for header in ('Date', 'Cache-Control', 'Server', 'Content-Type', 'Location'):
                    v = response.headers.get(header)
                    if v:
                        self.set_header(header, v)
                if response.body:
                    # Dump urls.
                    dt = Dumper(self.request.uri)
                    dt.start()
                    # Write threw.
                    self.write(response.body)
                self.finish()

        req = tornado.httpclient.HTTPRequest(
            url=self.request.uri,
            method=self.request.method,
            body=self.request.body,
            headers=self.request.headers,
            follow_redirects=False,
            allow_nonstandard_methods=True)
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            client.fetch(req, get_response)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                get_response(e.response)
            else:
                self.set_status(500)
                self.write('500 error:\n' + str(e))
                self.finish()
