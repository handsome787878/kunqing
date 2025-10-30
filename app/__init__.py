from flask import Flask, render_template_string
from flask_login import LoginManager
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 暂时回到简化模型，但使用SQLite确保数据持久化
    from .simple_models import init_sample_data, SimpleUser
    
    # 初始化Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "请先登录以访问此页面。"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return SimpleUser.get_by_id(int(user_id))

    # 初始化示例数据
    init_sample_data()

    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.simple_lost_found import lost_found_bp
    from .routes.simple_books import books_bp
    from .routes.simple_courses import courses_bp
    from .routes.simple_study_groups import study_groups_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(lost_found_bp, url_prefix="/lost_found")
    app.register_blueprint(books_bp, url_prefix="/books")
    app.register_blueprint(courses_bp, url_prefix="/courses")
    app.register_blueprint(study_groups_bp, url_prefix="/study_groups")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # 主页路由
    @app.route("/")
    def index():
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>鲲擎校园 - 校园生活助手</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        </head>
        <body>
            <div class="container">
                <div class="main-content">
                    <h1>🎓 鲲擎校园</h1>
                    <p>您的专属校园生活助手，让校园生活更便捷、更精彩！</p>
                    
                    <div class="nav-menu">
                        <div class="nav-card">
                            <a href="{{ url_for('auth.login') }}">
                                🔐 用户登录
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">登录您的账户</p>
                            </a>
                        </div>
                        
                        <div class="nav-card">
                            <a href="{{ url_for('auth.register') }}">
                                📝 用户注册
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">创建新账户</p>
                            </a>
                        </div>
                        
                        <div class="nav-card">
                            <a href="{{ url_for('lost_found.index') }}">
                                🔍 失物招领
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">找回丢失物品</p>
                            </a>
                        </div>
                        
                        <div class="nav-card">
                            <a href="{{ url_for('books.index') }}">
                                📚 二手书交易
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">买卖二手教材</p>
                            </a>
                        </div>
                        
                        <div class="nav-card">
                            <a href="{{ url_for('courses.index') }}">
                                🎯 课程评价
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">分享课程体验</p>
                            </a>
                        </div>
                        
                        <div class="nav-card">
                            <a href="{{ url_for('study_groups.index') }}">
                                👥 学习小组
                                <p style="font-size: 0.9rem; color: #666; margin-top: 10px;">组建学习团队</p>
                            </a>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 40px; color: #666;">
                        <p>💡 让我们一起创造更美好的校园生活体验</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """)

    return app