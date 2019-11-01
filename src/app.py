import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

#from handlers.displayhandler import DisplayHandler


class HomeHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("about.html", messages=None)

"""

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("connect.html", messages=None)

class DiscoverHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("discover.html", messages=None)


class DisplayHandler1(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("display.html", messages=None)
"""


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True,
            'template_path': os.path.join(os.path.dirname(__file__),
                                          "templates"),
            'static_path': os.path.join(os.path.dirname(__file__),
                                        "static")
        }
        handlers = [
            (r"/explorer/?", HomeHandler),
            (r"/explorer/static/(.*)",
             tornado.web.StaticFileHandler,
             {'path': settings['static_path']}),
            
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

"""
            (r"/explorer/connect/?", MainHandler),
            (r"/explorer/connect/static/(.*)",
             tornado.web.StaticFileHandler,
             {'path': settings['static_path']}),
            (r"/explorer/discover/?", DiscoverHandler),
            (r"/explorer/discover/static/(.*)",
             tornado.web.StaticFileHandler,
             {'path': settings['static_path']}),
            (r"/explorer/display1/?", DisplayHandler1),
            (r"/explorer/display1/static/(.*)",
             tornado.web.StaticFileHandler,
             {'path': settings['static_path']}),
            (r"/explorer/display/?", DisplayHandler),
            (r"/explorer/display/static/(.*)",
             tornado.web.StaticFileHandler,
             {'path': settings['static_path']}),
"""

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
