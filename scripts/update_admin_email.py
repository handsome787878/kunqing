#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新SQLAlchemy用户表中管理员（student_id='admin' 或 real_name='系统管理员'）的邮箱。

使用应用工厂以确保与当前配置一致（数据库：sqlite:///kunqing.sqlite）。
"""

import os
import sys

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.models import db, User

NEW_EMAIL = "2713878912@qq.com"


def update_admin_email():
    app = create_app()
    with app.app_context():
        # 优先按学号查找管理员，其次按真实姓名
        admin = User.query.filter_by(student_id="admin").first()
        if not admin:
            admin = User.query.filter_by(real_name="系统管理员").first()

        if not admin:
            print("[UpdateEmail] 未找到管理员用户（student_id='admin' 或 real_name='系统管理员'）")
            return

        # 检查新邮箱是否已被其他用户占用
        conflict = User.query.filter(User.email == NEW_EMAIL, User.id != admin.id).first()
        if conflict:
            print(f"[UpdateEmail] 新邮箱已被占用: {NEW_EMAIL}（用户ID={conflict.id}）")
            return

        old_email = admin.email
        admin.email = NEW_EMAIL
        try:
            db.session.commit()
            print(f"[UpdateEmail] 管理员邮箱更新成功: {old_email} -> {NEW_EMAIL}")
        except Exception as e:
            db.session.rollback()
            print(f"[UpdateEmail] 更新失败: {e}")


if __name__ == "__main__":
    update_admin_email()