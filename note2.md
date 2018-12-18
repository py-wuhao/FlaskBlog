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



