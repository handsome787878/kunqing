# 简化版数据模型，用于演示
from datetime import datetime


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


# 全局数据库实例
simple_db = SimpleDB()


class SimpleUser:
    """简化的用户模型"""
    
    def __init__(self, student_id, email, password, real_name=None):
        self.id = simple_db.get_next_id()
        self.student_id = student_id
        self.email = email
        self.password = password  # 实际应用中应该加密
        self.real_name = real_name
        self.college = ""
        self.major = ""
        self.grade = ""
        self.phone = ""
        self.avatar = ""
        self.create_time = datetime.now()
        self.last_login = None
        
        # 添加到数据库
        simple_db.users.append(self)
    
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
        return self.password == password
    
    @staticmethod
    def get_by_id(user_id):
        for user in simple_db.users:
            if user.id == int(user_id):
                return user
        return None
    
    @staticmethod
    def get_by_email(email):
        for user in simple_db.users:
            if user.email == email:
                return user
        return None


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
    if not simple_db.users:  # 只在第一次运行时初始化
        # 创建示例用户
        user1 = SimpleUser("2021001", "student1@example.com", "password123", "张三")
        user2 = SimpleUser("2021002", "student2@example.com", "password123", "李四")
        
        # 创建示例失物招领
        SimpleLostFound(user1.id, "lost", "丢失校园卡", "在图书馆丢失校园卡，卡号2021001", "图书馆", "13800138001")
        SimpleLostFound(user2.id, "found", "捡到钥匙", "在食堂捡到一串钥匙", "食堂", "13800138002")
        
        # 创建示例二手书
        SimpleBook(user1.id, "高等数学", "同济大学", 30, "八成新", "课本无笔记，保存完好")
        SimpleBook(user2.id, "大学英语", "外研社", 25, "九成新", "几乎全新")
        
        # 创建示例课程
        SimpleCourse("CS101", "计算机科学导论", "王教授", "计算机学院")
        SimpleCourse("MATH101", "高等数学", "李教授", "数学学院")
        
        # 创建示例学习小组
        SimpleStudyGroup(user1.id, "高数学习小组", "高等数学", "期末考试复习", 6)
        SimpleStudyGroup(user2.id, "英语口语练习", "英语", "提高口语水平", 4)