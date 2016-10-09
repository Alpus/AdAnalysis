class MainPage(tornado.web.RequestHandler):
    def get(self):
        self.render('Hello, Hell!')


routes = [
    (r'/', MainPage),
]