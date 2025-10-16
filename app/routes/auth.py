from flask import Blueprint, request, jsonify, render_template_string
from flask import redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, current_user

from ..simple_models import SimpleUser
from ..utils.decorators import login_required
from ..utils.helpers import (
    generate_captcha,
    store_captcha,
    verify_captcha,
    send_email,
)


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/")
def index():
    return render_template_string("""
    <h2>用户认证</h2>
    <p>当前用户: {{ current_user.real_name if current_user.is_authenticated else '未登录' }}</p>
    <ul>
        <li><a href="{{ url_for('auth.login') }}">登录</a></li>
        <li><a href="{{ url_for('auth.register') }}">注册</a></li>
        {% if current_user.is_authenticated %}
        <li><a href="{{ url_for('auth.profile') }}">个人资料</a></li>
        <li><a href="{{ url_for('auth.logout') }}">退出登录</a></li>
        {% endif %}
    </ul>
    <a href="{{ url_for('index') }}">返回首页</a>
    """)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        if not all([username, email, password, confirm_password]):
            if request.is_json:
                return jsonify({"error": "请填写所有字段"}), 400
            else:
                flash("请填写所有字段", "error")
                return redirect(url_for("auth.register"))
        
        if password != confirm_password:
            if request.is_json:
                return jsonify({"error": "两次输入的密码不一致"}), 400
            else:
                flash("两次输入的密码不一致", "error")
                return redirect(url_for("auth.register"))
        
        if SimpleUser.get_by_username(username):
            if request.is_json:
                return jsonify({"error": "用户名已存在"}), 400
            else:
                flash("用户名已存在", "error")
                return redirect(url_for("auth.register"))
        
        if SimpleUser.get_by_email(email):
            if request.is_json:
                return jsonify({"error": "邮箱已被注册"}), 400
            else:
                flash("邮箱已被注册", "error")
                return redirect(url_for("auth.register"))
        
        user = SimpleUser.create(username=username, email=email, password=password)
        if request.is_json:
            return jsonify({"message": "注册成功", "user_id": user.id}), 201
        else:
            flash("注册成功！请登录", "success")
            return redirect(url_for("auth.login"))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>用户注册 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h2>📝 用户注册</h2>
                <p>加入鲲擎校园，开启您的校园生活</p>
                
                <div class="form-container">
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">用户名</label>
                            <input type="text" id="username" name="username" required placeholder="请输入用户名">
                        </div>
                        
                        <div class="form-group">
                            <label for="email">邮箱</label>
                            <input type="email" id="email" name="email" required placeholder="请输入邮箱地址">
                        </div>
                        
                        <div class="form-group">
                            <label for="password">密码</label>
                            <input type="password" id="password" name="password" required placeholder="请输入密码">
                        </div>
                        
                        <div class="form-group">
                            <label for="confirm_password">确认密码</label>
                            <input type="password" id="confirm_password" name="confirm_password" required placeholder="请再次输入密码">
                        </div>
                        
                        <div class="form-group" style="text-align: center;">
                            <button type="submit" class="btn">注册</button>
                        </div>
                    </form>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <p>已有账户？ <a href="{{ url_for('auth.login') }}">立即登录</a></p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{{ url_for('index') }}" class="back-link">← 返回首页</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        username = data.get("username")
        password = data.get("password")
        
        if not all([username, password]):
            if request.is_json:
                return jsonify({"error": "请填写用户名和密码"}), 400
            else:
                flash("请填写用户名和密码", "error")
                return redirect(url_for("auth.login"))
        
        user = SimpleUser.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            if request.is_json:
                return jsonify({"message": "登录成功", "user_id": user.id})
            else:
                flash("登录成功！", "success")
                return redirect(url_for("index"))
        else:
            if request.is_json:
                return jsonify({"error": "用户名或密码错误"}), 401
            else:
                flash("用户名或密码错误", "error")
                return redirect(url_for("auth.login"))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>用户登录 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h2>🔐 用户登录</h2>
                <p>欢迎回来！请登录您的账户</p>
                
                <div class="form-container">
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">用户名</label>
                            <input type="text" id="username" name="username" required placeholder="请输入用户名">
                        </div>
                        
                        <div class="form-group">
                            <label for="password">密码</label>
                            <input type="password" id="password" name="password" required placeholder="请输入密码">
                        </div>
                        
                        <div class="form-group" style="text-align: center;">
                            <button type="submit" class="btn">登录</button>
                        </div>
                    </form>
                    
                    <div style="text-align: center; margin-top: 20px;">
                        <p>还没有账户？ <a href="{{ url_for('auth.register') }}">立即注册</a></p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{{ url_for('index') }}" class="back-link">← 返回首页</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template_string("""
    <h2>个人资料</h2>
    <p><strong>学号:</strong> {{ current_user.student_id }}</p>
    <p><strong>邮箱:</strong> {{ current_user.email }}</p>
    <p><strong>姓名:</strong> {{ current_user.real_name or '未设置' }}</p>
    <p><strong>注册时间:</strong> {{ current_user.create_time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
    <a href="{{ url_for('index') }}">返回首页</a>
    """)


@auth_bp.route("/send-reset-captcha", methods=["POST"])
def send_reset_captcha():
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "缺少邮箱"}), 400
    code = generate_captcha()
    store_captcha(email, code)
    ok = send_email(email, "密码重置验证码", f"您的验证码是：{code}")
    return jsonify({"sent": ok})


@auth_bp.route("/password-reset", methods=["GET", "POST"])
def password_reset():
    form = PasswordResetForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "用户不存在"}), 404
        if not verify_captcha(email, form.captcha.data):
            return jsonify({"error": "验证码错误或过期"}), 400
        user.set_password(form.new_password.data)
        db.session.commit()
        return jsonify({"message": "密码已重置"})

    return jsonify({"fields": ["email", "captcha", "new_password", "confirm_password"]})