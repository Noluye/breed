import tornado.ioloop
import tornado.web
from settings import port
from app import Application

if __name__ == "__main__":
    app = Application()
    app.listen(port)  # 只能在单进程模式中使用，等价如下
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.bind(8888)
    # http_server.start(1)
    tornado.ioloop.IOLoop.current().start()  # 循环询问linux-epoll
