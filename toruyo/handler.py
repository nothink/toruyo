
# -*- coding: utf-8 -*-

from .dumper.worker import Dumper

import sys
import os
import logging
import socket

import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.httpclient
import tornado.httputil


class ProxyHandler(tornado.web.RequestHandler):
    '''
    Proxy Handler Class
    '''
    SUPPORTED_METHODS = ("GET", "POST", "HEAD", "PUT", "CONNECT")

    # logger = None

    @tornado.web.asynchronous
    def get(self):
        '''
        GET request event handling　(Transparently).
        '''
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
            client.fetch(req, self.__handle_response, raise_error=False)
        except tornado.httpclient.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                self.__handle_response(e.response)
            else:
                self.set_status(500)
                self.write('500 Internal server error:\n' + str(e))
                self.finish()

    def __handle_response(self, response):
        '''
        Handling all response datas... and dump.
        '''
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

    # post : same as get
    post = get
    # head : same as get
    head = get
    # put : same as get
    put = get

    @tornado.web.asynchronous
    def connect(self):
        '''
        CONNECT request event handling　(Transparently).
        '''
        print('********************** CONNECT **********************')
        host, port = self.request.uri.split(':')
        client = self.request.connection.stream
        print('host: ' + host)
        print('port: ' + port)

        def read_from_client(data):
            upstream.write(data)

        def read_from_upstream(data):
            client.write(data)

        def client_close(data=None):
            if upstream.closed():
                return
            if data:
                upstream.write(data)
            upstream.close()

        def upstream_close(data=None):
            if client.closed():
                return
            if data:
                client.write(data)
            client.close()

        def start_tunnel():
#            logger.debug('CONNECT tunnel established to %s', self.request.uri)
            client.read_until_close(client_close, read_from_client)
            upstream.read_until_close(upstream_close, read_from_upstream)
            client.write(b'HTTP/1.0 200 Connection established\r\n\r\n')

        def on_proxy_response(data=None):
            if data:
                first_line = data.splitlines()[0]
                http_v, status, text = first_line.split(None, 2)
                if int(status) == 200:
#                    logger.debug('Connected to upstream proxy %s', proxy)
                    start_tunnel()
                    return

            self.set_status(500)
            self.finish()

        def start_proxy_tunnel():
            upstream.write('CONNECT %s HTTP/1.1\r\n' % self.request.uri)
            upstream.write('Host: %s\r\n' % self.request.uri)
            upstream.write('Proxy-Connection: Keep-Alive\r\n\r\n')
            upstream.read_until('\r\n\r\n', on_proxy_response)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        upstream = tornado.iostream.IOStream(s)
        upstream.connect((host, int(port)), start_tunnel)
