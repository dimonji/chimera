"""
Тестовый обработчик основных запросов.
"""

import json
from system.handlers import BaseHandler
from tornado.gen import coroutine


class TestHandler(BaseHandler):
    def data_received(self, chunk):
        print("data_received")
        pass

    @coroutine
    def get(self):
        print("get")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def post(self):
        print("post")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def put(self):
        print("put")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def delete(self):
        print("delete")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def head(self):
        print("head")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def options(self):
        print("options")
        self.write(json.dumps({"hello": "world"}))

    @coroutine
    def patch(self):
        print("patch")
        self.write(json.dumps({"hello": "world"}))