# -*- coding: utf-8 -*-
"""
    test
    ~~~~
    Flask-CORS is a simple extension to Flask allowing you to support cross
    origin resource sharing (CORS) using a simple decorator.

    :copyright: (c) 2014 by Cory Dolphin.
    :license: MIT, see LICENSE for more details.
"""

from tests.base_test import FlaskCorsTestCase
from flask import Flask

try:
    # this is how you would normally import
    from flask.ext.cors import *
except:
    # support local usage without installed package
    from flask_cors import *

class OriginsW3TestCase(FlaskCorsTestCase):
    def setUp(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        @cross_origin(origins='*', send_wildcard=False, always_send=False)
        def allowOrigins():
            ''' This sets up flask-cors to echo the request's `Origin` header,
                only if it is actually set. This behavior is most similar to
                the actual W3 specification, http://www.w3.org/TR/cors/ but
                is not the default because it is more common to use the
                wildcard configuration in order to support CDN caching.
            '''
            return 'Welcome!'

    def test_wildcard_origin_header(self):
        ''' If there is an Origin header in the request, the
            Access-Control-Allow-Origin header should be echoed back.
        '''
        example_origin = 'http://example.com'
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/', headers={'Origin': example_origin})
                self.assertEqual(
                    result.headers.get(ACL_ORIGIN),
                    example_origin
                )

    def test_wildcard_no_origin_header(self):
        ''' If there is no Origin header in the request, the
            Access-Control-Allow-Origin header should not be included.
        '''
        with self.app.test_client() as c:
            for verb in self.iter_verbs(c):
                result = verb('/')
                self.assertTrue(ACL_ORIGIN not in result.headers)


if __name__ == "__main__":
    unittest.main()
