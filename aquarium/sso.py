# -*- coding: utf-8 -*-
import os
import hashlib
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

import sys
if sys.version_info[0] > 2:
    from urllib.parse import parse_qs, urlparse
else:
    from urlparse import parse_qs, urlparse

class sso(object):
    """
    This class describes sso signin process
    """

    def __init__(self, parent=None):
        self.parent=parent

        self.verifier=None
        self.code=None
        self.server=None
        self.redirect=None

    def signin(self, redirect='http://localhost:8008'):
        self.redirect = redirect

        self.verifier = os.urandom(32).hex()

        verifierS256 = hashlib.sha256(self.verifier.encode('ascii')).digest()
        self.code = base64.urlsafe_b64encode(verifierS256).decode('ascii').rstrip('=')

        signin = self.parent.do_request('GET', 'sso/oidc/signin/url', params={'code': self.code, 'redirect': self.redirect})

        return signin

    def listen(self, port=8008, host='localhost', timeout=5):
        def handler(*args):
            serverHandler(self, *args)
        self.server = HTTPServer((host, port), handler)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        self.server.server_close()

    def callback(self, authorization):
        self.server.server_close()
        authorization['verifier'] = self.verifier
        authorization['redirect'] = self.redirect
        print('AUTH', authorization)

        result = self.parent.do_request('GET', 'sso/oidc/callback', params=authorization)
        token = result.pop("token")
        self.parent.token = token
        result = self.parent.element(result)

        return result
        # Start the HTTPServer in a new thread
        # server_thread = threading.Thread(target=self.server.serve_forever)
        # server_thread.daemon = True
        # server_thread.start()

        # time.sleep(timeout)

        # self.server.shutdown()
        # server_thread.join()
        # Start processing requests
        # self.thread = threading.Thread(None, self.server.run)
        # self.thread.start()

    # def stop(self):
    #     if (self.server is not None):
    #         self.server.shutdown()
    #         self.thread.join()

# class StoppableHTTPServer(HTTPServer):
#     def run(self):
#         try:
#             self.serve_forever()
#         except KeyboardInterrupt:
#             pass
#         finally:
#             # Clean-up server (close socket, etc.)
#             self.server_close()

class serverHandler(BaseHTTPRequestHandler):
    def __init__(self, sso=None, *args):
        self.sso=sso
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if (query['code'] is not None):
            self.sso.callback(query)
        self.send_response(200)
        self.end_headers()
        # self.server.shutdown()


