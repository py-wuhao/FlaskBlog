**跨站请求伪造CSRF**

恶意网站把请求发送到被攻击者已登录的其他网站时就会引发csrf攻击。

**表单类**

每个web表单都由一个继承Form的类表示。这个类定义表单中的一组字段，每个字段都用对象表示。字段对象可附属一个或多个验证函数。验证函数用来验证用户提交的输入值是否符合要求。

eg：

````python
from falsk.ext.wtf import From
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('What is you name?',validators=[Required()])
    subit = SubmitField('Submit')
````

|      字段类型       |              说明               |
| :-----------------: | :-----------------------------: |
|     StringField     |            文本字段             |
|    TxtAreaField     |          多行文本字段           |
|    PasswordField    |          密码文本字段           |
|     HiddenField     |          隐藏文本字段           |
|      DateField      |   文本字段，datetime.date格式   |
|    DateTimeField    | 文本字段，值为datetime.datetime |
|    IntegerField     |       文本字段，值为整数        |
|    DecimalField     |  文本字段，值为decimal.Decimal  |
|     FloatField      |      文本字段，值为浮点数       |
|    BooleanField     |     复选框，值为True和False     |
|     RadioField      |           一组单选框            |
|     SelectField     |            下拉列表             |
| SelectMultipleField |     下拉列表，可选择多个值      |
|      FileField      |          文件上传字段           |
|     SubmitField     |          表单提交按钮           |
|      FormField      |  把表单作为字段嵌入另一个表单   |
|      FieldList      |       一组指定类型的字段        |

| 验证函数    | 说明                                                   |
| ----------- | ------------------------------------------------------ |
| Email       | 验证电子邮箱地址                                       |
| EqualTo     | 比较两个字段的值，常用于要求输入两次密码进行确认的情况 |
| IPAddress   | 验证IPv4网络地址                                       |
| Length      | 验证输入字符串的长度                                   |
| NumberRange | 验证输入值在数字范围内                                 |
| Optional    | 无输入值时跳过其他验证函数                             |
| Required    | 确保字段中有数据                                       |
| Regexp      | 使用正则表达式验证输入值                               |
| URL         | 验证UR                                                 |
| AnyOf       | 确保输入值在可选值列表中                               |
| NoneOf      | 确保输入值不在可选列表中                               |

**重定向和用户会话**

浏览器刷新页面时会重新发送之前已发送的最后一个请求。如果这个请求是一个包含POST请求，刷新页面后会再次提交表单。

解决办法：使用重定向作为Post请求的响应，不使用常规响应。

````python
from flask import Flask, render_template, session, redirect, url_for
@app.route('/', methods=['GET', 'POST'])
def index():
    form NameForm()
    if form.validate_on_submit():
        session['name'] = form.naem.data
        return redirect(url_for('index'))
    return render_template('index.hrml', form=form, name=session.get('name'))
````

**flash消息**

flash('消息')

在heml中渲染 {% for message in get_flashed_messages() %}  {{message}}{% endfor %}

使用for是因为可能有多个消息排队

