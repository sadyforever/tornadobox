import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    def get(self):
        self.write("hello itcast.")

class UploadHandler(RequestHandler):
    def post(self):
        files = self.request.files


        # print(files) # {'key' : 'value'}
        # image_object = files['image']
        # print(type(image_object)) # []
        # print(type(image_object[0])) # {}  对象
        # print(image_object[0]['filename'])
        # print(image_object[0]['body'])
        # print(image_object[0]['content_type'])


        img_files = files.get('image')
        if img_files:
            img_file = img_files[0]["body"]
            # print(img_file)  # bytes
            file = open("./itcast.jpg", 'w+')
            file.write(img_file)
            file.close()
        self.write("OK")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/upload", UploadHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()