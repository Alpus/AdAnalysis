#!/usr/local/bin/python3
import tornado.ioloop
import tornado.web

from . import views
from .logic import functions
from . import settings


app = tornado.web.Application(views.routes, **settings.app_settings)

def run():
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run()