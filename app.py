import tornado.web
from handlers import index, dog
from settings import tornado_option


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/breed", index.MainHandler),
            (r'/breed/api/v1/dog', dog.JudgeDogHandler),
        ]
        super(Application, self).__init__(handlers, **tornado_option)
