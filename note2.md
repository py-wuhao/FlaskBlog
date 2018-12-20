**初始化**

web服务器使用web服务器网关接口协议（WSGI），把来自客户端所有的请求转交给flask类对象处理。

```python
from flask import Flask
app = Flask(__name__)

```

`__name__`参数决定程序的根目录



**视图和路由**

url到python函数的映射关系。

使用装饰器把修饰的函数注册为路由

````python
@app.route('/')
def index():
	return '<h1>hello wold!</h1>'
````

url中含有动态部分 使用 <变量名>,任何匹配静态部分的url都会映射到这个路由上，动态部分作为参数传入 动态部分可以指定类型

````python
@app.route('user/<name>')
def user(name):
    return '<h1>hello %s</h1>' % name
````

**启动服务器**

````python
if __name__ == '__main__':
	app.run(debug=True)
````

**程序和请求上下文**

flask使用上下文让特定变量在一个线程中全局可访问，不会干扰其他线程。

| current_app | 程序上下文 | 当前激活程序的程序实例                               |
| ----------- | ---------- | ---------------------------------------------------- |
| g           | 程序上下文 | 处理请求时用作临时存储对象，每次请求都会重设这个变量 |
| request     | 请求上下文 | 请求对象，封装了客户端发出的http请求中的内容         |
| session     | 请求上下文 | 用户会话，泳衣存储请求之间需要记住值的词典           |

**请求调度**

查看url映射: app.url_map 属性

**请求钩子**

请求钩子使用装饰器实现

before_first_request  注册一个函数，在第一个请求之前运行

before_request 注册一个函数，在每次请求之前运行

after_request 注册一个函数，如果没有异常抛出，在每次请求之后运行

teardown_request 注册一个函数，即使有未处理的异常抛出，也会在请求之后运行

---

请求钩子函数和视图函数之间一般使用上下文全局变量g

**响应**

响应由3部分组成，内容，状态码，响应头

生成响应对象 response = make_response(...)

response设置cookie  response.set_cookie(’answer‘，42)

重定向 状态码302

重定向函数 redirect('http://.....')

抛出异常函数 abort(404)

**使用flask—script支持命令行选项**

专为flask开发的扩展都暴露在flask.ext命名空间下



**flask-bootstrap组件**

用于创建简洁具有吸引力的网页









