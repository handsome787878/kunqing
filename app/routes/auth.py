from flask import Blueprint, request, jsonify, render_template_string
from flask import redirect, url_for, render_template, flash, session
import time
from flask_login import login_user, logout_user, current_user
from datetime import datetime

from ..models import db, User
from ..utils.decorators import login_required
from ..utils.helpers import (
    generate_captcha,
    store_captcha,
    verify_captcha,
    send_email,
    send_verification_email,
)
from ..forms.auth import RegisterForm, LoginForm, ProfileForm, PasswordResetForm


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/")
def index():
    return render_template("auth/index.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # JSON API 提交
    if request.method == "POST" and request.is_json:
        data = request.get_json() or {}
        student_id = data.get("student_id") or data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password") or password
        captcha = data.get("captcha")

        if not all([student_id, email, password, confirm_password]):
            return jsonify({"error": "请填写所有字段"}), 400
        if password != confirm_password:
            return jsonify({"error": "两次输入的密码不一致"}), 400
        if User.query.filter_by(student_id=student_id).first():
            return jsonify({"error": "学号已存在"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "邮箱已被注册"}), 400
        if captcha and not verify_captcha(email, captcha):
            return jsonify({"error": "验证码不正确或已失效"}), 400
        user = User(student_id=student_id, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "注册成功", "user_id": user.id}), 201

    # 表单提交
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            student_id = form.student_id.data.strip()
            email = form.email.data.strip()
            password = form.password.data
            captcha = form.captcha.data.strip()

            # 唯一性校验
            if User.query.filter_by(student_id=student_id).first():
                flash("该学号已存在", "error")
                return render_template("auth/register.html", form=form)
            if User.query.filter_by(email=email).first():
                flash("该邮箱已被注册", "error")
                return render_template("auth/register.html", form=form)
            # 验证码校验
            if not verify_captcha(email, captcha):
                flash("验证码不正确或已失效", "error")
                return render_template("auth/register.html", form=form)

            # 创建用户（SQLAlchemy）
            try:
                user = User(student_id=student_id, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash("注册成功！请登录", "success")
                return redirect(url_for("auth.login"))
            except Exception:
                db.session.rollback()
                flash("注册失败，请稍后重试", "error")
                return render_template("auth/register.html", form=form)
        else:
            # 表单校验失败
            return render_template("auth/register.html", form=form)

    # GET 渲染
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # JSON API 提交
    if request.method == "POST" and request.is_json:
        data = request.get_json() or {}
        account = (
            data.get("account")
            or data.get("username")
            or data.get("student_id")
            or data.get("email")
        )
        password = data.get("password")

        if not account or not password:
            return jsonify({"error": "请填写账号和密码"}), 400

        # 支持学号或邮箱（SQLAlchemy）
        user = User.query.filter((User.student_id == account) | (User.email == account)).first()
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({"message": "登录成功", "user_id": user.id})
        return jsonify({"error": "账号或密码错误"}), 401

    # 表单提交
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            account = form.account.data.strip()
            password = form.password.data
            remember = form.remember_me.data

            user = User.query.filter((User.student_id == account) | (User.email == account)).first()
            if user and user.check_password(password):
                login_user(user, remember=remember)
                user.last_login = datetime.utcnow()
                db.session.commit()
                flash("登录成功！", "success")
                return redirect(url_for("index"))
            else:
                flash("账号或密码错误", "error")
                return render_template("auth/login.html", form=form)
        else:
            # 校验失败，回显错误
            return render_template("auth/login.html", form=form)

    # GET 渲染
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("已退出登录", "info")
    return redirect(url_for("index"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # 保存到数据库（SQLAlchemy）
            try:
                current_user.real_name = form.real_name.data.strip() if form.real_name.data else None
                current_user.college = form.college.data.strip() if form.college.data else None
                current_user.major = form.major.data.strip() if form.major.data else None
                current_user.grade = form.grade.data.strip() if form.grade.data else None
                current_user.phone = form.phone.data.strip() if form.phone.data else None
                db.session.commit()
                flash("资料已保存", "success")
            except Exception:
                db.session.rollback()
                flash("保存失败，请稍后重试", "error")
        else:
            flash("请检查表单输入", "error")
    else:
        # GET 时预填充当前用户信息
        form.real_name.data = getattr(current_user, "real_name", "") or ""
        form.college.data = getattr(current_user, "college", "") or ""
        form.major.data = getattr(current_user, "major", "") or ""
        form.grade.data = getattr(current_user, "grade", "") or ""
        form.phone.data = getattr(current_user, "phone", "") or ""

    return render_template("auth/profile.html", form=form)


@auth_bp.route("/send-reset-captcha", methods=["POST"])
def send_reset_captcha():
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "缺少邮箱"}), 400
    # 简易冷却：同一会话 60 秒
    now = time.time()
    last = session.get("reset_last_sent_ts")
    if last and now - last < 60:
        remaining = int(60 - (now - last))
        return jsonify({"error": f"请稍后再试（{remaining}秒）"}), 429
    code = generate_captcha()
    store_captcha(email, code)
    ok = send_email(email, "密码重置验证码", f"您的验证码是：{code}")
    if ok:
        session["reset_last_sent_ts"] = now
    return jsonify({"sent": ok})


@auth_bp.route("/send-register-captcha", methods=["POST"])
def send_register_captcha():
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "缺少邮箱"}), 400
    ok = send_verification_email(email)
    return jsonify({"sent": ok})


@auth_bp.route("/password-reset", methods=["GET", "POST"])
def password_reset():
    # JSON API 提交
    if request.method == "POST" and request.is_json:
        data = request.get_json() or {}
        email = data.get("email")
        captcha = data.get("captcha")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password") or new_password

        if not all([email, captcha, new_password, confirm_password]):
            return jsonify({"error": "请填写所有字段"}), 400
        if new_password != confirm_password:
            return jsonify({"error": "两次密码不一致"}), 400
        if not verify_captcha(email, captcha):
            return jsonify({"error": "验证码不正确或已失效"}), 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "邮箱未注册"}), 404
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "密码重置成功"}), 200

    # 表单提交
    form = PasswordResetForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data.strip()
            captcha = form.captcha.data.strip()
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            if new_password != confirm_password:
                flash("两次密码不一致", "error")
                return render_template("auth/password_reset.html", form=form)
            if not verify_captcha(email, captcha):
                flash("验证码不正确或已失效", "error")
                return render_template("auth/password_reset.html", form=form)
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("该邮箱未注册", "error")
                return render_template("auth/password_reset.html", form=form)

            user.set_password(new_password)
            db.session.commit()
            flash("密码已重置，请使用新密码登录", "success")
            return redirect(url_for("auth.login"))
        else:
            return render_template("auth/password_reset.html", form=form)

    # GET 渲染
    return render_template("auth/password_reset.html", form=form)