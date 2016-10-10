import tornado.ioloop
import tornado.web

from . import views
from . import models

app = tornado.web.Application(views.routes, cookie_secret="42")

def run():
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    run()