#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_user():
    """创建管理员用户"""
    # 获取当前脚本所在的目录 (d:\kunqing-a\kunqing)
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 拼接数据库路径
    db_path = os.path.join(basedir, 'kunqing.sqlite') # 确保这里的文件名和 config.py 里的一模一样！

    print(f"正在连接数据库: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建管理员用户
    password = 'admin123'
    password_hash = generate_password_hash(password)
    
    cursor.execute('''
        INSERT OR REPLACE INTO users (student_id, email, password_hash, real_name, create_time, admin_level)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', password_hash, '系统管理员', datetime.now(), 2))
    
    conn.commit()
    conn.close()
    print('管理员用户创建完成: admin / admin123')

if __name__ == '__main__':
    create_admin_user()