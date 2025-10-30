"""管理员权限装饰器"""

from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def admin_required(func):
    """要求管理员权限的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录", "error")
            return redirect(url_for("auth.login"))
        
        if not current_user.is_admin_user():
            flash("您没有管理员权限", "error")
            abort(403)
        
        return func(*args, **kwargs)
    return wrapper


def super_admin_required(func):
    """要求超级管理员权限的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录", "error")
            return redirect(url_for("auth.login"))
        
        if not current_user.is_super_admin():
            flash("您没有超级管理员权限", "error")
            abort(403)
        
        return func(*args, **kwargs)
    return wrapper


def user_management_required(func):
    """要求用户管理权限的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录", "error")
            return redirect(url_for("auth.login"))
        
        if not current_user.can_manage_users():
            flash("您没有用户管理权限", "error")
            abort(403)
        
        return func(*args, **kwargs)
    return wrapper


def content_management_required(func):
    """要求内容管理权限的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("请先登录", "error")
            return redirect(url_for("auth.login"))
        
        if not current_user.can_manage_content():
            flash("您没有内容管理权限", "error")
            abort(403)
        
        return func(*args, **kwargs)
    return wrapper