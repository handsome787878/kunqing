#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建示例用户数据脚本
"""

import sys
import os
from datetime import datetime, timedelta
import random

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User

def create_sample_users():
    """创建示例用户数据"""
    
    # 示例用户数据
    sample_users = [
        {
            'student_id': '2021001001',
            'email': 'zhangsan@kunqing.edu.cn',
            'real_name': '张三',
            'college': '计算机科学与技术学院',
            'major': '计算机科学与技术',
            'grade': '2021级',
            'phone': '13800138001',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2021001002',
            'email': 'lisi@kunqing.edu.cn',
            'real_name': '李四',
            'college': '软件工程学院',
            'major': '软件工程',
            'grade': '2021级',
            'phone': '13800138002',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2020001003',
            'email': 'wangwu@kunqing.edu.cn',
            'real_name': '王五',
            'college': '信息管理学院',
            'major': '信息管理与信息系统',
            'grade': '2020级',
            'phone': '13800138003',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2022001004',
            'email': 'zhaoliu@kunqing.edu.cn',
            'real_name': '赵六',
            'college': '电子信息工程学院',
            'major': '电子信息工程',
            'grade': '2022级',
            'phone': '13800138004',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2021001005',
            'email': 'sunqi@kunqing.edu.cn',
            'real_name': '孙七',
            'college': '数学与统计学院',
            'major': '数学与应用数学',
            'grade': '2021级',
            'phone': '13800138005',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2020001006',
            'email': 'zhouba@kunqing.edu.cn',
            'real_name': '周八',
            'college': '物理与电子工程学院',
            'major': '应用物理学',
            'grade': '2020级',
            'phone': '13800138006',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2022001007',
            'email': 'wujiu@kunqing.edu.cn',
            'real_name': '吴九',
            'college': '化学与材料工程学院',
            'major': '化学工程与工艺',
            'grade': '2022级',
            'phone': '13800138007',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2021001008',
            'email': 'zhengshi@kunqing.edu.cn',
            'real_name': '郑十',
            'college': '生命科学学院',
            'major': '生物技术',
            'grade': '2021级',
            'phone': '13800138008',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2020001009',
            'email': 'chenyi@kunqing.edu.cn',
            'real_name': '陈一',
            'college': '外国语学院',
            'major': '英语',
            'grade': '2020级',
            'phone': '13800138009',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': '2022001010',
            'email': 'liuer@kunqing.edu.cn',
            'real_name': '刘二',
            'college': '经济管理学院',
            'major': '工商管理',
            'grade': '2022级',
            'phone': '13800138010',
            'is_admin': False,
            'admin_level': 0
        },
        {
            'student_id': 'admin001',
            'email': 'admin@kunqing.edu.cn',
            'real_name': '系统管理员',
            'college': '信息中心',
            'major': '系统管理',
            'grade': '管理员',
            'phone': '13800000001',
            'is_admin': True,
            'admin_level': 2
        },
        {
            'student_id': 'admin002',
            'email': 'moderator@kunqing.edu.cn',
            'real_name': '内容审核员',
            'college': '学生事务处',
            'major': '内容管理',
            'grade': '管理员',
            'phone': '13800000002',
            'is_admin': True,
            'admin_level': 1
        }
    ]
    
    created_count = 0
    
    for user_data in sample_users:
        # 检查用户是否已存在
        existing_user = User.query.filter(
            (User.student_id == user_data['student_id']) | 
            (User.email == user_data['email'])
        ).first()
        
        if existing_user:
            print(f"用户 {user_data['real_name']} ({user_data['student_id']}) 已存在，跳过创建")
            continue
        
        # 创建新用户
        user = User(
            student_id=user_data['student_id'],
            email=user_data['email'],
            real_name=user_data['real_name'],
            college=user_data['college'],
            major=user_data['major'],
            grade=user_data['grade'],
            phone=user_data['phone'],
            is_admin=user_data['is_admin'],
            admin_level=user_data['admin_level'],
            create_time=datetime.now() - timedelta(days=random.randint(1, 365)),
            last_login=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        
        # 设置默认密码（实际项目中应该要求用户首次登录时修改）
        default_password = '123456'
        user.set_password(default_password)
        
        try:
            db.session.add(user)
            db.session.commit()
            created_count += 1
            print(f"✅ 创建用户: {user.real_name} ({user.student_id}) - {user.email}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ 创建用户失败: {user.real_name} - {str(e)}")
    
    print(f"\n🎉 成功创建 {created_count} 个示例用户！")
    print("\n📋 用户列表:")
    print("=" * 80)
    print(f"{'学号':<12} {'姓名':<8} {'邮箱':<25} {'学院':<15} {'角色':<8}")
    print("=" * 80)
    
    users = User.query.all()
    for user in users:
        role = "超级管理员" if user.admin_level == 2 else "管理员" if user.admin_level == 1 else "普通用户"
        print(f"{user.student_id:<12} {user.real_name:<8} {user.email:<25} {user.college[:12]:<15} {role:<8}")
    
    print("=" * 80)
    print(f"总计: {len(users)} 个用户")
    print("\n💡 默认密码: 123456")
    print("🔐 管理员账号:")
    print("   - admin@kunqing.edu.cn (超级管理员)")
    print("   - moderator@kunqing.edu.cn (普通管理员)")


def main():
    """主函数"""
    app = create_app()
    
    with app.app_context():
        print("🚀 开始创建示例用户数据...")
        print("=" * 50)
        
        # 确保数据库表已创建
        try:
            db.create_all()
            print("✅ 数据库表检查完成")
        except Exception as e:
            print(f"❌ 数据库表创建失败: {str(e)}")
            return
        
        # 创建示例用户
        create_sample_users()


if __name__ == '__main__':
    main()