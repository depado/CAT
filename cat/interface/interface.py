#!/usr/bin/env python3
# coding: utf-8

import os

import bottle
from bottle import Bottle, view, static_file

DIRECTORY = os.path.dirname(__file__)
os.chdir(DIRECTORY)

bottle.debug = True

bottle.TEMPLATE_PATH = [DIRECTORY + '/views']


class CatInterface(Bottle):
    def __init__(self):
        super().__init__()

        @self.route('/')
        @view('main_page')
        def main_page():
            pass

        @self.route('/static/asset/<file>')
        def static_image(file):
            return static_file(file, root='views/asset')

        @self.route('/static/style/<file>')
        def static_stylesheet(file):
            return static_file(file, root='views/style')

    def run(self, host='localhost', port=8080, **kwds):
        super().run(host=host, port=port, **kwds)