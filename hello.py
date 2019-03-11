import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options
import textwrap

define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ", friendly user!")

    def write_error(self, status_code, **kwargs):
        self.write('Gosh darnit, user! You caused a %d error.' % status_code)


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, width))


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler)
    ])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
