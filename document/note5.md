**SQL数据库**

关系型数据库把数据存储在表中，表模拟程序中不同的实体。表可以有称为外键的列，这是关系型数据库模型的基础。

**NOSQL数据库**

一般使用集合代替表，使用文档代替记录

**ORM**

对象关系映射，把高层的面向对象操作转换为低层的数据库指令

**Flask-SQLAlcheny**

这是一个强大的关系型数据库框架，支持多种数据库后台。提供高层的ORM，也提供使用原生SQL的低层功能

SQLALCEMY_COMMIT_ON_TEARDOWN=True 每次请求结束后都会自动提交数据库中的变动。

````python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
````

**SQLAlchem列类型**

| 类型名       | Python类型         | 说　　明                                              |
| ------------ | ------------------ | ----------------------------------------------------- |
| Integer      | int                | 普通整数，一般是 32 位                                |
| SmallInteger | int                | 取值范围小的整数，一般是 16 位                        |
| BigInteger   | int 或 long        | 不限制精度的整数                                      |
| Float        | float              | 浮点数                                                |
| Numeric      | decimal.Decimal    | 定点数                                                |
| String       | str                | 变长字符串                                            |
| Text         | str                | 变长字符串，对较长或不限长度的字符串做了优化          |
| Unicode      | unicode            | 变长 Unicode 字符串                                   |
| UnicodeText  | unicode            | 变长 Unicode 字符串，对较长或不限长度的字符串做了优化 |
| Boolean      | bool               | 布尔值                                                |
| Date         | datetime.date      | 日期                                                  |
| Time         | datetime.time      | 时间                                                  |
| DateTime     | datetime.datetime  | 日期和时间                                            |
| Interval     | datetime.timedelta | 时间间隔                                              |
| Enum         | str                | 一组字符串                                            |
| PickleType   | 任何 Python 对象   | 自动使用 Pickle 序列化                                |
| LargeBinary  | str                | 二进制文件                                            |

**SQLAlchemy列选项**

| 选项名      | 说　　明                                                     |
| ----------- | ------------------------------------------------------------ |
| primary_key | 如果设为 True ，这列就是表的主键                             |
| unique      | 如果设为 True ，这列不允许出现重复的值                       |
| index       | 如果设为 True ，为这列创建索引，提升查询效率                 |
| nullable    | 如果设为 True ，这列允许使用空值；如果设为 False ，这列不允许使用空值 |
| default     | 为这列定义默认值                                             |

**插入行**

````python
from hello import Role, User
admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)
````

通过数据库会话管理对数据库改动。把要写入的对象先添加到会话中db.session.add(object),然后提交db.session.commit()

数据库会话也称为事务，保证了数据库的一致性提交操作使用原子方式把会话中的对象全部写入数据库中。如果发生错误整个会话都会失效。

**集成python shell**

让Flask-Script的shell命令自动导入特定的对象

使用 app.shell_context_processor 装饰器创建并注册
一个 shell 上下文处理器

````python
@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role)
````

**flask-migrate实现数据库迁移**

配置flask-migrate

````python
from flask.ext.migrate import Migrate,MigrateCommand
# ...
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
````

迁移前创建迁移仓库 init

upgrade()函数将迁移中的改动应用到数据库中

downgrade函数将改动删除

