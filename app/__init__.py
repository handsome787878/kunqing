from flask import Flask, render_template, render_template_string, session
from flask_login import LoginManager
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 接入 SQLAlchemy（正式模型）并兼容简化模型
    from .models import db, User, School
    from .simple_models import init_sample_data, SimpleUser
    
    # 初始化 SQLAlchemy
    db.init_app(app)
    
    # 初始化Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录以访问此页面。"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        # 优先使用 SQLAlchemy 的 User 模型（1.x 兼容写法），失败时退回简化模型
        try:
            uid = int(user_id)
            sa_user = User.query.get(uid)
            if sa_user:
                return sa_user
        except Exception:
            pass
        return SimpleUser.get_by_id(int(user_id))

    # 初始化示例数据
    init_sample_data()

    # 模板过滤器：相对时间显示（timeago），支持语言与时区
    from datetime import datetime, timedelta
    def timeago(dt):
        try:
            if not dt:
                return "从未登录"

            # 配置读取（支持国际化与时区）
            locale = app.config.get("TIMEAGO_LOCALE", "zh")
            tz_offset_minutes = int(app.config.get("TIMEAGO_TZ_OFFSET_MINUTES", 0))

            # 以 UTC 为基准，应用时区偏移
            now_utc = datetime.utcnow() + timedelta(minutes=tz_offset_minutes)

            # 处理传入时间（可能为 naive 或 aware）
            dt_base = dt
            try:
                if getattr(dt, "tzinfo", None) is not None:
                    # 简化处理：将 aware 时间视为本地，统一应用偏移
                    dt_base = dt
            except Exception:
                dt_base = dt

            dt_local = dt_base + timedelta(minutes=tz_offset_minutes)
            diff = now_utc - dt_local
            seconds = max(0, int(diff.total_seconds()))

            # 不同语言的单位
            if locale == "en":
                if seconds < 60:
                    return "just now"
                minutes = seconds // 60
                if minutes < 60:
                    return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
                hours = minutes // 60
                if hours < 24:
                    return f"{hours} hour{'s' if hours != 1 else ''} ago"
                days = hours // 24
                if days < 30:
                    return f"{days} day{'s' if days != 1 else ''} ago"
                months = days // 30
                if months < 12:
                    return f"{months} month{'s' if months != 1 else ''} ago"
                years = months // 12
                return f"{years} year{'s' if years != 1 else ''} ago"
            else:
                if seconds < 60:
                    return "刚刚"
                minutes = seconds // 60
                if minutes < 60:
                    return f"{minutes} 分钟前"
                hours = minutes // 60
                if hours < 24:
                    return f"{hours} 小时前"
                days = hours // 24
                if days < 30:
                    return f"{days} 天前"
                months = days // 30
                if months < 12:
                    return f"{months} 个月前"
                years = months // 12
                return f"{years} 年前"
        except Exception:
            return "未知"

    app.add_template_filter(timeago, name="timeago")

    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.simple_lost_found import lost_found_bp
    from .routes.simple_books import books_bp
    from .routes.simple_courses import courses_bp
    from .routes.simple_study_groups import study_groups_bp
    from .routes.admin import admin_bp
    from .routes.school import school_bp

    # 蓝图自身已定义 url_prefix，这里不再重复传入，以避免路径前缀叠加
    app.register_blueprint(auth_bp)
    app.register_blueprint(lost_found_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(study_groups_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(school_bp)

    # 主页路由
    @app.route("/")
    def index():
        return render_template("home.html")

    @app.context_processor
    def inject_current_school():
        """在模板上下文提供当前选择的学校对象"""
        try:
            sid = session.get("current_school_id")
            current_school = School.query.get(sid) if sid else None
        except Exception:
            current_school = None
        return {"current_school": current_school}
        

    return app