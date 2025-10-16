import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 基础配置
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG = True

    # 数据库配置（SQLite）- 简化版本用于演示
    SQLITE_DB_FILENAME = os.environ.get("SQLITE_DB_FILENAME", "kunqing.sqlite")
    SQLITE_DB_PATH = os.path.join(basedir, SQLITE_DB_FILENAME)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # 邮件配置（用于注册验证和密码找回）
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@example.com")

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "images", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB 图片大小限制
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # 会话配置
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # 开发环境下为 False，生产环境建议 True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"