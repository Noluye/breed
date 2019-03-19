import tornado.ioloop
import tornado.web
import tornado.httpserver
from settings import port
from app import Application
from settings import ssl_options

if __name__ == "__main__":
    app = Application()
    server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
    server.listen(port)
    tornado.ioloop.IOLoop.current().start()  # 循环询问linux-epoll
