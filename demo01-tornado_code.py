
import tornado.web
import tornado.ioloop
                                # tornado 框架中request和response都封装到  RequestHandler类中
class IndexHandler(tornado.web.RequestHandler):
    '''主页处理类'''
    def get(self):
        '''get请求方式'''
        self.write('hello world')


if __name__ == '__main__':
                    # application接口     路由列表
    app = tornado.web.Application([(r'/',IndexHandler)])
    # 创建一个http服务器实例,绑定端口listen(port,ip)
    app.listen(8070)
    # 最关键的一步 , 异步高并发就是ioloop实现的
    tornado.ioloop.IOLoop.current().start()
            # ioloop模块的  IOloop类 中的 current方法 : 创建线程的IOLoop实例
                            # start方法启动IOLoop实例的I/O循环,同时服务器监听被打开
