#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建SQLite数据库并添加示例用户
"""

import os
import sys
import sqlite3
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'kunqing.sqlite')

def init_database():
    """初始化SQLite数据库"""
    print("正在初始化数据库...")
    
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
            last_login TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("数据库表创建完成")

def create_sample_users():
    """创建示例用户"""
    print("正在创建示例用户...")
    
    # 简单的密码哈希（实际项目中应使用bcrypt）
    import hashlib
    
    def simple_hash(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 示例用户数据
    users = [
        # 管理员账户
        ('admin', 'admin@kunqing.edu.cn', '123456', '系统管理员', '信息技术部', '系统管理', '管理员', '13800000000'),
        ('admin001', 'admin001@kunqing.edu.cn', '123456', '张管理', '教务处', '教务管理', '管理员', '13800000001'),
        
        # 学生账户
        ('2021001', 'student1@kunqing.edu.cn', '123456', '张三', '计算机学院', '软件工程', '2021级', '13800000101'),
        ('2021002', 'student2@kunqing.edu.cn', '123456', '李四', '计算机学院', '计算机科学与技术', '2021级', '13800000102'),
        ('2021003', 'student3@kunqing.edu.cn', '123456', '王五', '电子工程学院', '电子信息工程', '2021级', '13800000103'),
        ('2022001', 'student4@kunqing.edu.cn', '123456', '赵六', '机械工程学院', '机械设计制造及其自动化', '2022级', '13800000201'),
        ('2022002', 'student5@kunqing.edu.cn', '123456', '钱七', '经济管理学院', '工商管理', '2022级', '13800000202'),
    ]
    
    for student_id, email, password, real_name, college, major, grade, phone in users:
        try:
            password_hash = simple_hash(password)
            cursor.execute('''
                INSERT INTO users (student_id, email, password_hash, real_name, college, major, grade, phone, create_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, email, password_hash, real_name, college, major, grade, phone, datetime.now()))
            print(f"创建用户: {student_id} ({real_name})")
        except sqlite3.IntegrityError:
            print(f"用户 {student_id} 已存在，跳过")
    
    conn.commit()
    conn.close()
    print("示例用户创建完成")

def main():
    """主函数"""
    print("=== 鲲擎校园系统数据库初始化 ===")
    
    # 检查数据库是否已存在
    if os.path.exists(DB_PATH):
        print(f"数据库文件已存在: {DB_PATH}")
        response = input("是否要重新初始化数据库？(y/N): ")
        if response.lower() != 'y':
            print("取消初始化")
            return
        else:
            os.remove(DB_PATH)
            print("已删除旧数据库文件")
    
    # 初始化数据库
    init_database()
    
    # 创建示例用户
    create_sample_users()
    
    print("\n=== 初始化完成 ===")
    print("可用的测试账户:")
    print("管理员账户:")
    print("  用户名: admin, 密码: admin123 (管理员级别: 2)")
    print("学生账户:")
    print("  用户名: 2021001, 密码: password123 (张三)")
    print("  用户名: 2021002, 密码: password123 (李四)")
    print("  用户名: 2022001, 密码: password123 (赵六)")
    print("\n现在可以启动应用程序: python run.py")

if __name__ == '__main__':
    main()