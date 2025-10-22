from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import bcrypt
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    real_name = db.Column(db.String(50))
    college = db.Column(db.String(100))
    major = db.Column(db.String(100))
    grade = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    last_login = db.Column(db.DateTime)

    # 关系
    lost_founds = db.relationship(
        "LostFound",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    secondhand_books = db.relationship(
        "SecondhandBook",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    book_messages = db.relationship(
        "BookMessage",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    course_reviews = db.relationship(
        "CourseReview",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    study_groups = db.relationship(
        "StudyGroup",
        backref=db.backref("owner", lazy=True),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    group_memberships = db.relationship(
        "GroupMember",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User id={self.id} student_id={self.student_id} email={self.email}>"

    # 密码处理
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))
        except ValueError:
            return False

    # Flask-Login 要求的方法
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)


class LostFound(db.Model):
    __tablename__ = "lost_found"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    type = db.Column(db.String(10), nullable=False)  # lost / found
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    lost_time = db.Column(db.DateTime)
    contact = db.Column(db.String(200))
    images = db.Column(db.JSON, default=list)  # 图片列表
    status = db.Column(db.String(20), default="open")
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    update_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<LostFound id={self.id} type={self.type} title={self.title}>"


class SecondhandBook(db.Model):
    __tablename__ = "secondhand_books"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    book_name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(20), index=True)
    publisher = db.Column(db.String(100))
    course = db.Column(db.String(100))
    college = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    condition = db.Column(db.String(50))
    description = db.Column(db.Text)
    images = db.Column(db.JSON, default=list)
    status = db.Column(db.String(20), default="available")
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # 关系：书籍留言
    messages = db.relationship(
        "BookMessage",
        backref="book",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<SecondhandBook id={self.id} name={self.book_name} price={self.price}>"


class BookMessage(db.Model):
    __tablename__ = "book_messages"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("secondhand_books.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<BookMessage id={self.id} book_id={self.book_id} user_id={self.user_id}>"


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    course_name = db.Column(db.String(200), nullable=False)
    teacher = db.Column(db.String(100))
    college = db.Column(db.String(100))
    credit = db.Column(db.Float)
    description = db.Column(db.Text)

    # 关系：课程评价
    reviews = db.relationship(
        "CourseReview",
        backref="course",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Course id={self.id} code={self.course_code} name={self.course_name}>"


class CourseReview(db.Model):
    __tablename__ = "course_reviews"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    rating = db.Column(db.Integer)  # 评分
    difficulty = db.Column(db.Integer)  # 难度
    workload = db.Column(db.Integer)  # 负担
    content = db.Column(db.Text)
    exam_info = db.Column(db.Text)
    study_tips = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<CourseReview id={self.id} course_id={self.course_id} user_id={self.user_id}>"


class StudyGroup(db.Model):
    __tablename__ = "study_groups"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100))
    goal = db.Column(db.Text)
    plan = db.Column(db.Text)
    target_members = db.Column(db.Integer)
    current_members = db.Column(db.Integer, default=0)
    requirements = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="open")
    create_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # 关系：小组成员
    members = db.relationship(
        "GroupMember",
        backref="group",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<StudyGroup id={self.id} title={self.title} subject={self.subject}>"


class GroupMember(db.Model):
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("study_groups.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    role = db.Column(db.String(50))
    join_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    status = db.Column(db.String(20), default="active")

    def __repr__(self):
        return f"<GroupMember id={self.id} group_id={self.group_id} user_id={self.user_id} role={self.role}>"