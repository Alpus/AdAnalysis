import tornado

class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render('implementation.html')


routes = [
    (r'/', MainPage),
]