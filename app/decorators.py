# 检查用户权限装饰器
from functools import wraps

from flask_login import current_user
from werkzeug.exceptions import abort

from app.models import Permission


def permission_required(permission):
    """
    带参数装饰器
    :param permission:
    :return: 装饰器
    """

    def decorator(f):
        @wraps(f)
        def decorators_function(*args, **kwargs):
            if not current_user.role.hash_permission(permission):
                abort(403)  # 禁止访问
            return f(*args, **kwargs)

        return decorators_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
