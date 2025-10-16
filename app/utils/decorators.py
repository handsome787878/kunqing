"""自定义装饰器，包括登录校验。"""

from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return func(*args, **kwargs)

    return wrapper