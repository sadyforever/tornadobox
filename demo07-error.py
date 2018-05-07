
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('主页')
        self.send_error(404, content="出现404错误")
        self.write("结束")
if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/',IndexHandler)
    ],debug=True)
    http_server = HTTPServer(app)
    http_server.listen(8000)
    IOLoop.current().start()