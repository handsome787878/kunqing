# 简化版数据模型，用于演示
from datetime import datetime
import sqlite3
import os
from datetime import datetime

# SQLite数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kunqing.sqlite')

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


class SimpleDB:
    """简单的内存数据库，用于演示"""
    
    def __init__(self):
        self.users = []
        self.lost_found = []
        self.books = []
        self.courses = []
        self.study_groups = []
        self._id_counter = 1
    
    def get_next_id(self):
        current_id = self._id_counter
        self._id_counter += 1
        return current_id
    
    def get_all_users(self):
        """获取所有用户"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()
        
        users = []
        for row in rows:
            # 数据库字段顺序: id, student_id, email, password_hash, real_name, college, major, grade, phone, avatar, create_time, last_login, admin_level
            user_dict = {
                'id': row[0],
                'student_id': row[1],
                'email': row[2],
                'password_hash': row[3],
                'real_name': row[4],
                'college': row[5],
                'major': row[6],
                'grade': row[7],
                'phone': row[8],
                'avatar': row[9],
                'create_time': row[10],
                'last_login': row[11],
                'admin_level': row[12] if len(row) > 12 else 0,
                'is_active': True  # 默认为活跃用户
            }
            users.append(user_dict)
        
        return users


# 全局数据库实例
simple_db = SimpleDB()


class SimpleUser:
    """简化的用户模型"""
    
    def __init__(self, id, student_id, email, password_hash, real_name=None, college=None, major=None, grade=None, phone=None, avatar=None, create_time=None, last_login=None, admin_level=0):
        self.id = id
        self.student_id = student_id
        self.email = email
        self.password_hash = password_hash
        self.real_name = real_name
        self.college = college
        self.major = major
        self.grade = grade
        self.phone = phone
        self.avatar = avatar
        self.create_time = create_time
        self.last_login = last_login
        self.admin_level = admin_level
        
        # 添加到数据库（已在create方法中处理）
        pass
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def check_password(self, password):
        """验证密码"""
        # 兼容历史数据：优先按 bcrypt 校验；若为旧版 SHA256，则回退并自动迁移为 bcrypt
        import bcrypt, hashlib, sqlite3
        stored = self.password_hash or ""
        try:
            if stored.startswith("$2"):
                # bcrypt 格式
                return bcrypt.checkpw(password.encode('utf-8'), stored.encode('utf-8'))
            else:
                # 旧版 hex(SHA256)
                sha_hex = hashlib.sha256(password.encode('utf-8')).hexdigest()
                if sha_hex == stored:
                    # 成功后迁移为 bcrypt，提升安全性
                    try:
                        new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        conn = sqlite3.connect(DB_PATH)
                        cur = conn.cursor()
                        cur.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, self.id))
                        conn.commit()
                        conn.close()
                        self.password_hash = new_hash
                    except Exception:
                        # 迁移失败不影响当前登录
                        pass
                    return True
                return False
        except Exception:
            return False
    
    def is_admin_user(self):
        """检查是否为管理员用户"""
        # 简化版：学号以admin开头或特定学号为管理员
        admin_accounts = ['admin', 'admin001', '2021001']  # 可以根据需要添加更多管理员账号
        return self.student_id in admin_accounts or self.student_id.startswith('admin')
    
    def can_manage_content(self):
        """检查是否可以管理内容"""
        # 管理员用户可以管理内容
        return self.is_admin_user()
    
    def can_manage_users(self):
        """检查是否可以管理用户"""
        # 管理员用户可以管理用户
        return self.is_admin_user()
    
    def is_super_admin(self):
        """检查用户是否是超级管理员"""
        # 检查admin_level
        if hasattr(self, 'admin_level') and self.admin_level >= 2:
            return True
        
        # 特殊账号处理：admin账号直接给予超级管理员权限
        if self.student_id == 'admin':
            return True
            
        return False
    
    @staticmethod
    def create(student_id, email, password):
        """创建新用户并保存到SQLite数据库"""
        import bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (student_id, email, password_hash, create_time, admin_level)
                VALUES (?, ?, ?, ?, ?)
            ''', (student_id, email, password_hash, datetime.now(), 0))
            
            user_id = cursor.lastrowid
            conn.commit()
            
            # 返回新创建的用户对象
            user = SimpleUser(user_id, student_id, email, password_hash, create_time=datetime.now(), admin_level=0)
            return user
            
        except sqlite3.IntegrityError:
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_username(student_id):
        """根据学号获取用户"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE student_id = ?', (student_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 数据库字段顺序: id, student_id, email, password_hash, real_name, college, major, grade, phone, avatar, create_time, last_login, admin_level
            return SimpleUser(
                id=row[0],
                student_id=row[1], 
                email=row[2],
                password_hash=row[3],
                real_name=row[4],
                college=row[5],
                major=row[6],
                grade=row[7],
                phone=row[8],
                avatar=row[9],
                create_time=row[10],
                last_login=row[11],
                admin_level=row[12] if len(row) > 12 else 0
            )
        return None

    @staticmethod
    def get_by_email(email):
        """根据邮箱获取用户"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 数据库字段顺序: id, student_id, email, password_hash, real_name, college, major, grade, phone, avatar, create_time, last_login
            return SimpleUser(
                id=row[0],
                student_id=row[1], 
                email=row[2],
                password_hash=row[3],
                real_name=row[4],
                college=row[5],
                major=row[6],
                grade=row[7],
                phone=row[8],
                avatar=row[9],
                create_time=row[10],
                last_login=row[11]
            )
        return None

    @staticmethod
    def get_by_id(user_id):
        """根据ID获取用户"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # 数据库字段顺序: id, student_id, email, password_hash, real_name, college, major, grade, phone, avatar, create_time, last_login
            return SimpleUser(
                id=row[0],
                student_id=row[1], 
                email=row[2],
                password_hash=row[3],
                real_name=row[4],
                college=row[5],
                major=row[6],
                grade=row[7],
                phone=row[8],
                avatar=row[9],
                create_time=row[10],
                last_login=row[11]
            )
        return None

    @staticmethod
    def update_profile(user_id, real_name=None, college=None, major=None, grade=None, phone=None):
        """更新用户资料并返回最新的用户对象"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 仅更新提供的字段
        fields = []
        values = []
        if real_name is not None:
            fields.append('real_name = ?')
            values.append(real_name)
        if college is not None:
            fields.append('college = ?')
            values.append(college)
        if major is not None:
            fields.append('major = ?')
            values.append(major)
        if grade is not None:
            fields.append('grade = ?')
            values.append(grade)
        if phone is not None:
            fields.append('phone = ?')
            values.append(phone)

        if not fields:
            conn.close()
            return SimpleUser.get_by_id(user_id)

        sql = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        values.append(user_id)
        cursor.execute(sql, tuple(values))
        conn.commit()
        conn.close()

        # 返回最新的用户对象
        return SimpleUser.get_by_id(user_id)

    @staticmethod
    def update_password(user_id, new_password):
        """更新用户密码为 bcrypt 哈希"""
        import bcrypt
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (password_hash, user_id))
        conn.commit()
        conn.close()
        return True
    

class SimpleLostFound:
    """简化的失物招领模型"""
    
    def __init__(self, user_id, type, title, description="", location="", contact=""):
        self.id = simple_db.get_next_id()
        self.user_id = user_id
        self.type = type  # 'lost' or 'found'
        self.title = title
        self.description = description
        self.location = location
        self.contact = contact
        self.status = "open"
        self.create_time = datetime.now()
        
        # 添加到数据库
        simple_db.lost_found.append(self)
    
    @staticmethod
    def get_all():
        return simple_db.lost_found
    
    @staticmethod
    def get_by_id(item_id):
        for item in simple_db.lost_found:
            if item.id == int(item_id):
                return item
        return None


class SimpleBook:
    """简化的二手书模型"""
    
    def __init__(self, user_id, book_name, author="", price=0, condition="", description=""):
        self.id = simple_db.get_next_id()
        self.user_id = user_id
        self.book_name = book_name
        self.author = author
        self.price = price
        self.condition = condition
        self.description = description
        self.status = "available"
        self.create_time = datetime.now()
        
        # 添加到数据库
        simple_db.books.append(self)
    
    @staticmethod
    def get_all():
        return simple_db.books
    
    @staticmethod
    def get_by_id(book_id):
        for book in simple_db.books:
            if book.id == int(book_id):
                return book
        return None


class SimpleCourse:
    """简化的课程模型"""
    
    def __init__(self, course_code, course_name, teacher="", college=""):
        self.id = simple_db.get_next_id()
        self.course_code = course_code
        self.course_name = course_name
        self.teacher = teacher
        self.college = college
        self.description = ""
        
        # 添加到数据库
        simple_db.courses.append(self)
    
    @staticmethod
    def get_all():
        return simple_db.courses
    
    @staticmethod
    def get_by_id(course_id):
        for course in simple_db.courses:
            if course.id == int(course_id):
                return course
        return None


class SimpleStudyGroup:
    """简化的学习小组模型"""
    
    def __init__(self, user_id, title, subject="", goal="", target_members=5):
        self.id = simple_db.get_next_id()
        self.user_id = user_id
        self.title = title
        self.subject = subject
        self.goal = goal
        self.target_members = target_members
        self.current_members = 1  # 创建者自动加入
        self.status = "open"
        self.create_time = datetime.now()
        
        # 添加到数据库
        simple_db.study_groups.append(self)
    
    @staticmethod
    def get_all():
        return simple_db.study_groups
    
    @staticmethod
    def get_by_id(group_id):
        for group in simple_db.study_groups:
            if group.id == int(group_id):
                return group
        return None


# 初始化一些示例数据
def init_sample_data():
    """初始化示例数据"""
    init_db()  # 确保数据库表已创建
    
    # 检查是否已有用户数据
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        # 创建示例用户
        SimpleUser.create("2021001", "student1@example.com", "password123")
        SimpleUser.create("2021002", "student2@example.com", "password123")
        print("已创建示例用户数据")