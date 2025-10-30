#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
import bcrypt

DB_PATH = 'simple_campus.db'

def init_db():
    """初始化SQLite数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            real_name TEXT,
            college TEXT,
            major TEXT,
            grade TEXT,
            phone TEXT,
            avatar TEXT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            admin_level INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    print('数据库初始化完成')

def create_admin_user():
    """创建管理员用户"""
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
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
    init_db()
    create_admin_user()