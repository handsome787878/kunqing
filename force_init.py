import os
import sys
from werkzeug.security import generate_password_hash

# 尝试导入 db，处理不同的项目结构
try:
    from app import create_app, db
    print("成功从 app 导入 db")
except ImportError:
    try:
        from exts import db
        from app import create_app
        print("成功从 exts 导入 db")
    except ImportError:
        try:
            from app.models import db
            from app import create_app
            print("成功从 app.models 导入 db")
        except ImportError:
            # 如果都找不到，尝试在 create_app 内部查找
            from app import create_app
            print("将在 app context 中查找 db")
            db = None

from app.models import User

# 1. 创建应用上下文
app = create_app()

# 如果上面没找到 db，尝试从 app 扩展中获取
if db is None:
    if hasattr(app, 'extensions') and 'sqlalchemy' in app.extensions:
        db = app.extensions['sqlalchemy'].db
    else:
        # 最后的尝试：直接看 app 模块里有没有
        import app as app_module
        if hasattr(app_module, 'db'):
            db = app_module.db
        else:
            print("错误：无法找到 SQLAlchemy db 对象，请检查代码结构。")
            sys.exit(1)

# 确保使用正确的数据库文件
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'kunqing.sqlite')
print(f"目标数据库路径: {db_path}")

with app.app_context():
    # 2. 暴力重置：删除所有表并重新创建
    print("正在删除旧表...")
    db.drop_all()
    
    print("正在根据 models.py 创建新表...")
    db.create_all()
    print("表结构创建成功！")

    # 3. 使用 ORM 方式添加管理员
    print("正在创建管理员账号...")
    
    user_data = {
        'student_id': 'admin',
        'email': 'admin@example.com',
        'real_name': '系统管理员',
        'password_hash': generate_password_hash('admin123'),
        'is_admin': True,
        'college': '管理学院',
        'major': '系统管理',
        'grade': '2021',
        'phone': '13800138000'
    }
    
    if hasattr(User, 'admin_level'):
        user_data['admin_level'] = 2
        print("检测到 admin_level 字段，已设置为 2")
    
    admin = User(**user_data)

    db.session.add(admin)
    db.session.commit()
    
    print("="*30)
    print("初始化全部完成！")
    print("请使用以下账号登录：")
    print("账号: admin")
    print("密码: admin123")
    print("="*30)