**flask组成：**

​	路由，调试和web服务器网关接口子系统由Werkzeug提供；模板系统有Jinja提供。

​	flask原生不支持数据库访问，web表单验证和用户认证等高级功能。需要的核心服务都以扩展的形式实现，然后在与核心包集成。

**虚拟环境使用**

作用：避免包混乱和版本冲突，为每个程序单独创建虚拟环境可以保证程序只访问虚拟环境中的包。保证全局解释器的干净整洁

检查安装：virtualenv --version

安装工具：sudo apt-get install python-virtualenv

安装虚拟环境： virtualenv  enev  -p python3

​						环境名和版本

激活环境：source venv/bin/activate

退出环境：deactivate



