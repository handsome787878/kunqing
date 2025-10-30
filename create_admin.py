#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
import bcrypt

def create_admin_user():
    """创建管理员用户"""
    # 连接数据库
    conn = sqlite3.connect('simple_campus.db')
    cursor = conn.cursor()
    
    # 创建管理员用户
    password = 'admin123'
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    cursor.execute('''
        INSERT OR REPLACE INTO users (student_id, email, password_hash, real_name, create_time, admin_level)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('admin', 'admin@example.com', password_hash, '系统管理员', datetime.now(), 2))
    
    conn.commit()
    conn.close()
    print('管理员用户创建完成: admin / admin123')

if __name__ == '__main__':
    create_admin_user()