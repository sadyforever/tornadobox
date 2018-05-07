'''
tornado.options模块   命令行传参
定义 define   定义之后可以通过命令行传参启动
取出 parse_command_line           定义和取出应该是同时出现的,没有传入就使用默认但是必须有取出的函数
使用 tornado.options.options.变量方法

导入其他模块 tornado.options.parse_config_file(path路径)
可以把配置统一写在其他文件,通过导入文件
'''

# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options # 新导入的options模块

# define函数 定义的变量可以在全局的tornado.options.options对象中获取使用
tornado.options.define("port", default=8000, type=int, help="run server on the given port.") # 定义服务器监听端口选项
tornado.options.define(name="itcast", default=[], type=str, multiple=True, help="itcast subjects.") # 无意义，演示多值情况
# define(变量名, 默认值, 类型, multiple是否可以为多个,True那么default就是[]了, 提示信息)


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        """对应http的get请求方式"""
        self.write("Hello Itcast!")

if __name__ == "__main__":
    # tornado.options.parse_command_line() 和 define应该是同时出现的
    # 取出命令行参数  传参方式 --port=9000
    tornado.options.parse_command_line()

    print (tornado.options.options.itcast) # 就为了检验itcast



    app = tornado.web.Application([
        (r"/", IndexHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)

                                # define定义的变量是对象属性
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()