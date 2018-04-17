# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver # 新引入httpserver模块

class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    # ------------------------------
    # 我们修改这个部分
    # app.listen(8000)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8000)
    # 实际是由HTPPServer实例化服务器对象,把接口路由映射传进去
    # 而 http_server.listen(8000) 其实由
    # http_server.bind(8000)
    # http_server.start(1)  默认开启一个进程
    # app.listen()只能用于单进程模式
    # ------------------------------
    tornado.ioloop.IOLoop.current().start()

'''
多进程:
    虽然tornado给我们提供了一次开启多个进程的方法，但是由于：

    每个子进程都会从父进程中复制一份IOLoop实例，如过在创建子进程前我们的代码动了IOLoop实例，那么会影响到每一个子进程，势必会干扰到子进程IOLoop的工作；
    所有进程是由一个命令一次开启的，也就无法做到在不停服务的情况下更新代码；
    所有进程共享同一个端口，想要分别单独监控每一个进程就很困难。
    不建议使用这种多进程的方式，而是手动开启多个进程，并且绑定不同的端口。
'''