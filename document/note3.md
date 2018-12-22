**渲染模板**

渲染模板使用 render_template(模板文件名，参数名)

**过滤器**

使用 | 我理解为管道连接符

| 过滤器名   | 说明               |
| ---------- | ------------------ |
| safe       | 渲染时不转意       |
| capitalize | 首字母大写         |
| lower      | 转换为小写         |
| upper      | 转换为大写         |
| title      | 每个单词首字母大写 |
| trim       | 去掉首尾空格       |
| striptags  | 删除所有html标签   |

**控制结构**

TODO  笔记版某些按键不灵

if

for

macro 类似定义函数

import

include

blocck  extends

**自定义错误页面**

````python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

````

**链接**

url_for(视图，参数，_external)  返回路由。_external=True返回绝对路径

**flask-moment插件本地化日期和时间**

