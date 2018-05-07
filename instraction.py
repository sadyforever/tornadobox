# 创建新的虚拟环境,pip install tornado
main_thing = 'tornado框架'

'''
1.tornado.web
 1-1 RequestHandler  
        get方法,post方法 和 write 来给出响应内容
 1-2 Application  接口保存路由  
        创建的app  listen方法开启Http服务器
        
2.tornado.ioloop
 ioloop工作原理:监听socket,当有事件发生时,把内容给到Application的路由去处理,然后路由给到处理的视图
 2-1 IOLoop.current() IOLoop实例
 2-2 IOLoop.start()  启动IOLoop实例的I/O循环,同时服务器监听被打开
'''


'''
3.httpserver对象
app.listen(8000) 是封装创建服务器的方法
实际 http_server = tornado.httpserver.HTTPServer(app) 
    http_server.listen(8000)
而 listen又是封装的方法
实际是 http_server.bind(8000)
      http_server.start(1)
而 start方法中可以指定开启几个进程 0:根据cpu核心数, 1:开启1个
      
'''


'''
4.options 全局参数定义、存储、转换 (port灵活手动传入)   其实就是命令行传参

tornado.options模块   命令行传参
定义 define   定义之后可以通过命令行传参启动
# define(变量名, 默认值, 类型, multiple是否可以为多个,True那么default就是[]了, 提示信息)

取出 parse_command_line           定义和取出应该是同时出现的,没有传入就使用默认但是必须有取出的函数
使用 tornado.options.options.变量方法

导入其他模块 tornado.options.parse_config_file(path路径)
可以把配置统一写在其他文件,通过导入文件
'''


'''
5.日志
当我们使用命令行的时候tornado默认开启logging功能
关闭:options.logging = None

配置:  实际开发是从外部导入config文件,  在Application的第二个参数 **config.settings

'''


'''
6.Application 第一个参数 路由列表 []

一个路由是一个元组

(r"/", ItcastHandler, {"subject":"c++"})
元组的第三个元素,可以在视图类中获取到 (路由中的字典，会传入到对应的RequestHandler的initialize()方法中)
class ItcastHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)
        
url(r"/python", ItcastHandler, {"subject":"python"}, name="python_url")
当使用name起名字的时候,前边必须使用url
url_map的使用 : RequestHandler.reverse_url(name)来获取该名字对应的url
'''


'''
7.request
tornado使用视图类,但是不像django在def方法中有request参数,tornado只有self就可以,所以使用获取参数的方法时:self.get_argument
7-1. 查询字符串参数 ?后边的  a=1&b=2&c=3&a=4    
get_query_argument(参数名,'')  默认有个空,避免报错  同名的获取最后一个
get_query_arguments(参数名)  返回结果是list,获取不到是空[]

7-2. 请求体   不能获取json和xml
get_body_argument(参数名,'')
get_body_arguments(参数名)

 封装成
get_argument
get_arguments

7-3.其他
method 请求方式;
host 被请求的主机名；
uri 请求的完整资源标示，包括路径和查询字符串；
path 请求的路径部分；
query 请求的查询字符串部分；
version 使用的HTTP版本；
headers 请求的协议头，是类字典型的对象，支持关键字索引的方式获取特定协议头信息，例如：request.headers["Content-Type"]
body 请求体数据；
remote_ip 客户端的IP地址；

files 获取到用户上传的文件,是字典格式 ,通过key拿到value,是个列表
通过 list[0]拿到里边的对象字典,可以当做字典来操作
对象字典是 HTTPFile对象,有3个属性,通过属性获取相应的内容 (filename 文件的实际名字,body 文件的数据实体,content_type 文件的类型)

files = self.request.files 拿到文件
img_files = files.get('img')  # get('key')  得到的是list
if img_files:
    img_file = img_files[0]["body"] 是个列表,所以[0]拿出对象字典,然后用body拿出内容
    
7-4./index/user/login  这种写在url中的和django相同,可以正则匹配,然后放到def get函数的参数中,也分为起名字?P<name>和没名字两种,位置对应
'''


'''
8.response          tornado的响应使用self没有什么对象的操作不像django的HTTPResponse

8-1.响应内容  write方法是把响应内容写到缓存区,所以可以多次写,一次一起返回

原本: json格式
stu = {
    "name":"zhangsan",
    "age":24,
    "gender":1,
}
stu_json = json.dumps(stu)  # 把字典用python内置json模块dumps成json
self.write(stu_json)

但是write方法,自带识别字典自动转换  

8-2.响应头 set_header(name, value)
set_default_headers()视图类中的方法,重写此方法来预先设置默认的headers
def set_default_headers(self):
    self.set_header("Content-Type", "application/json")
    
8-3.状态码 set_status(num)

8-4.重定向 redirect

8-5.异常 
    抛出异常send_error(status_code,**kwargs)     如果继续write的话崩了
    
    但是第二个参数,自定义的错误信息,并不能给到浏览器
    需要重新 write_error(self, status_code, **kwargs)方法
    因为在类中所以有self,**kwargs可以写很多内容,用key取出来
    self.send_error(err_code, title=err_title, content=err_content)
    
    def write_error(self, status_code, **kwargs):
        self.write("错误名：%s" % kwargs["title"])
        self.write("错误详情：%s" % kwargs["content"])
'''


'''
9.执行顺序 (执行顺序决定钩子问题,选择性重写)
初始化 def initialize(self) 很少使用

执行对应请求方式前,执行预处理  def prepare(self)   (钩子:request_before)

在请求处理结束后调用 def on_finish(self) (钩子:request_after)

注意:set_default_headers() 设置头 在initialize之前调用 
    但是如果有报错,那么在set_error 之后又调用一次来重新设置头

'''