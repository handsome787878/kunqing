"""管理员后台路由"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.utils.admin_decorators import admin_required, super_admin_required, user_management_required, content_management_required
from app.simple_models import SimpleUser, SimpleLostFound, SimpleBook
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    """管理员登录页面"""
    if request.method == "POST":
        account = request.form.get("account", "").strip()
        password = request.form.get("password", "")
        
        if not account or not password:
            flash("请填写完整的登录信息", "error")
            return render_template("admin/login.html")
        
        # 查找用户（支持学号或邮箱登录）
        user = SimpleUser.get_by_username(account) or SimpleUser.get_by_email(account)
        
        if not user or not user.check_password(password):
            flash("账号或密码错误", "error")
            return render_template("admin/login.html")
        
        # 检查管理员权限
        if not user.is_admin_user():
            flash("您没有管理员权限", "error")
            return render_template("admin/login.html")
        
        # 登录成功
        login_user(user, remember=True)
        user.last_login = datetime.now()
        
        flash(f"欢迎回来，{user.real_name or user.student_id}！", "success")
        return redirect(url_for("admin.dashboard"))
    
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@login_required
def admin_logout():
    """管理员登出"""
    logout_user()
    flash("已安全退出管理后台", "info")
    return redirect(url_for("admin.admin_login"))


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    """管理员后台首页"""
    # 简化版统计数据（使用示例数据）
    stats = {
        'total_users': 5,
        'total_lost_found': 8,
        'total_books': 12,
        'total_reviews': 15,
        'total_groups': 6,
        'new_users_today': 2,
        'active_lost_found': 5,
        'available_books': 8,
    }
    
    # 简化版最近活动数据
    recent_users = []
    recent_lost_found = []
    recent_books = []
    
    return render_template("admin/dashboard.html", 
                         stats=stats,
                         recent_users=recent_users,
                         recent_lost_found=recent_lost_found,
                         recent_books=recent_books)


@admin_bp.route("/users")
@user_management_required
def users():
    """用户管理页面"""
    # 简化版用户管理 - 创建示例用户数据
    sample_users = [
        {
            'id': 1,
            'student_id': '2021001',
            'email': 'student1@example.com',
            'real_name': '张三',
            'college': '计算机学院',
            'major': '计算机科学与技术',
            'grade': '2021级',
            'phone': '13800138001',
            'create_time': datetime.now(),
            'last_login': datetime.now(),
            'is_admin': True,
            'admin_level': 1,
            'status': 'active'
        },
        {
            'id': 2,
            'student_id': '2021002',
            'email': 'student2@example.com',
            'real_name': '李四',
            'college': '信息学院',
            'major': '软件工程',
            'grade': '2021级',
            'phone': '13800138002',
            'create_time': datetime.now(),
            'last_login': datetime.now(),
            'is_admin': False,
            'admin_level': 0,
            'status': 'active'
        },
        {
            'id': 3,
            'student_id': '2021003',
            'email': 'student3@example.com',
            'real_name': '王五',
            'college': '电子学院',
            'major': '电子信息工程',
            'grade': '2021级',
            'phone': '13800138003',
            'create_time': datetime.now(),
            'last_login': datetime.now(),
            'is_admin': False,
            'admin_level': 0,
            'status': 'active'
        },
        {
            'id': 4,
            'student_id': '2021004',
            'email': 'student4@example.com',
            'real_name': '赵六',
            'college': '机械学院',
            'major': '机械设计制造及其自动化',
            'grade': '2021级',
            'phone': '13800138004',
            'create_time': datetime.now(),
            'last_login': datetime.now(),
            'is_admin': False,
            'admin_level': 0,
            'status': 'inactive'
        },
        {
            'id': 5,
            'student_id': 'admin',
            'email': 'admin@example.com',
            'real_name': '系统管理员',
            'college': '管理部门',
            'major': '系统管理',
            'grade': '管理员',
            'phone': '13800138000',
            'create_time': datetime.now(),
            'last_login': datetime.now(),
            'is_admin': True,
            'admin_level': 2,
            'status': 'active'
        }
    ]
    
    # 创建一个简单的分页对象模拟
    class SimplePagination:
        def __init__(self, items):
            self.items = items
            self.total = len(items)
            self.page = 1
            self.per_page = 20
            self.pages = 1
            self.has_prev = False
            self.has_next = False
            self.prev_num = None
            self.next_num = None
    
    users = SimplePagination(sample_users)
    search = request.args.get('search', '')
    admin_filter = request.args.get('admin_filter', '')
    
    return render_template("admin/users.html", users=users, search=search, admin_filter=admin_filter)


@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@user_management_required
def user_detail(user_id):
    """用户详情页面"""
    from app.simple_models import SimpleDB
    
    db = SimpleDB()
    users = db.get_all_users()
    
    # 查找指定用户
    user = None
    for u in users:
        if u.get('id') == user_id:
            user = u
            break
    
    if not user:
        flash('用户不存在', 'error')
        return redirect(url_for('admin.users'))
    
    # 模拟用户对象，添加必要的属性
    class MockUser:
        def __init__(self, data):
            self.id = data.get('id')
            self.student_id = data.get('student_id')
            self.email = data.get('email')
            self.is_active = data.get('is_active', True)
            self.is_admin = data.get('is_admin', False)
            self.admin_level = data.get('admin_level', 0)
            self.created_at = None  # 简化模型中没有这个字段
            self.last_login = None  # 简化模型中没有这个字段
            # 模拟关联数据
            self.lost_found_items = []
            self.secondhand_books = []
            self.course_reviews = []
            self.study_groups = []
    
    mock_user = MockUser(user)
    
    if request.method == 'POST':
        # 处理用户信息更新
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        is_active = request.form.get('is_active') == '1'
        admin_level = int(request.form.get('admin_level', 0))
        
        # 更新用户信息
        user['student_id'] = student_id
        user['email'] = email
        user['is_active'] = is_active
        user['admin_level'] = admin_level
        user['is_admin'] = admin_level > 0
        
        # 在实际应用中，这里应该保存到数据库
        flash('用户信息已更新', 'success')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    
    # 获取用户的相关数据
    user_stats = {
        'lost_found_count': 0,
        'books_count': 0,
        'reviews_count': 0,
        'groups_count': 0,
    }
    
    return render_template("admin/user_detail.html", user=mock_user, user_stats=user_stats)


@admin_bp.route("/users/<int:user_id>/toggle_admin", methods=["POST"], endpoint="toggle_admin")
@super_admin_required
def toggle_user_admin(user_id):
    """切换用户管理员状态"""
    # 简化版：返回成功消息
    return jsonify({"message": f"用户管理员状态切换功能暂未实现", "is_admin": False})


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@super_admin_required
def delete_user(user_id):
    """删除用户"""
    # 简化版：返回成功消息
    return jsonify({"message": f"用户删除功能暂未实现"})


@admin_bp.route("/content")
@content_management_required
def content():
    """内容管理页面"""
    # 获取待审核的内容 - 使用简化版本
    all_lost_found = SimpleLostFound.get_all()
    all_books = SimpleBook.get_all()
    
    # 计算待处理的数量（简化版本中没有pending状态，使用open/available状态）
    pending_lost_found = len([item for item in all_lost_found if item.status == 'open'])
    pending_books = len([book for book in all_books if book.status == 'available'])
    
    return render_template("admin/content_management.html", 
                         pending_lost_found=pending_lost_found,
                         pending_books=pending_books)


@admin_bp.route("/content/lost_found")
@content_management_required
def lost_found_management():
    """失物招领管理"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    # 使用简化版本获取数据
    all_items = SimpleLostFound.get_all()
    if status_filter:
        all_items = [item for item in all_items if item.status == status_filter]
    
    # 简单分页处理
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    items = all_items[start:end]
    
    # 创建简单的分页对象
    class SimplePagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
    
    lost_found_items = SimplePagination(items, page, per_page, len(all_items))
    
    return render_template("admin/lost_found_management.html", 
                         items=lost_found_items, 
                         status_filter=status_filter)


@admin_bp.route("/content/books")
@content_management_required
def books_management():
    """二手书管理"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    # 使用简化版本获取数据
    all_books = SimpleBook.get_all()
    if status_filter:
        all_books = [book for book in all_books if book.status == status_filter]
    
    # 简单分页处理
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    book_items = all_books[start:end]
    
    # 创建简单的分页对象
    class SimplePagination:
        def __init__(self, items, page, per_page, total):
            self.items = items
            self.page = page
            self.per_page = per_page
            self.total = total
            self.pages = (total + per_page - 1) // per_page
            self.has_prev = page > 1
            self.has_next = page < self.pages
            self.prev_num = page - 1 if self.has_prev else None
            self.next_num = page + 1 if self.has_next else None
    
    books = SimplePagination(book_items, page, per_page, len(all_books))
    
    return render_template("admin/books_management.html", 
                         books=books, 
                         status_filter=status_filter)


@admin_bp.route('/content/lost_found/<int:item_id>/approve', methods=['POST'])
@content_management_required
def approve_lost_found(item_id):
    """审核通过失物招领"""
    # 在实际应用中，这里应该更新数据库中的状态
    flash(f'失物招领 #{item_id} 已审核通过', 'success')
    return redirect(url_for('admin.content'))

@admin_bp.route('/content/lost_found/<int:item_id>/reject', methods=['POST'])
@content_management_required
def reject_lost_found(item_id):
    """拒绝失物招领"""
    reason = request.form.get('reason', '不符合发布规范')
    # 在实际应用中，这里应该更新数据库中的状态并记录拒绝原因
    flash(f'失物招领 #{item_id} 已拒绝：{reason}', 'warning')
    return redirect(url_for('admin.content'))

@admin_bp.route('/content/books/<int:book_id>/approve', methods=['POST'])
@content_management_required
def approve_book(book_id):
    """审核通过二手书"""
    # 在实际应用中，这里应该更新数据库中的状态
    flash(f'二手书 #{book_id} 已审核通过', 'success')
    return redirect(url_for('admin.content'))

@admin_bp.route('/content/books/<int:book_id>/reject', methods=['POST'])
@content_management_required
def reject_book(book_id):
    """拒绝二手书"""
    reason = request.form.get('reason', '不符合发布规范')
    # 在实际应用中，这里应该更新数据库中的状态并记录拒绝原因
    flash(f'二手书 #{book_id} 已拒绝：{reason}', 'warning')
    return redirect(url_for('admin.content'))


@admin_bp.route('/statistics')
@admin_required
def statistics():
    """数据统计页面"""
    from app.simple_models import SimpleDB
    
    # 获取统计数据
    db = SimpleDB()
    users = db.get_all_users()
    
    # 计算统计指标
    total_users = len(users)
    active_users = len([u for u in users if u.get('is_active', True)])
    
    # 模拟其他统计数据
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users_growth': 12,
        'total_posts': 3456,
        'monthly_posts': 234,
        'posts_growth': 8,
        'activity_rate': 71.5,
        'daily_active': 456,
        'activity_growth': 5.2,
        'success_rate': 68.3,
        'successful_deals': 189,
        'success_growth': 3.1
    }
    
    return render_template('admin/statistics.html', stats=stats)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@super_admin_required
def settings():
    """系统设置页面"""
    if request.method == 'POST':
        # 处理设置保存逻辑
        site_name = request.form.get('site_name')
        site_description = request.form.get('site_description')
        contact_email = request.form.get('contact_email')
        timezone = request.form.get('timezone')
        
        # 这里可以将设置保存到数据库或配置文件
        flash('设置已保存', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html')


@admin_bp.route('/settings/test-smtp', methods=['POST'])
@super_admin_required
def test_smtp():
    """测试当前 SMTP 配置并返回结果（含耗时与错误信息）。"""
    # 获取测试收件人
    email = request.form.get('email')
    if request.is_json and not email:
        data = request.get_json() or {}
        email = data.get('email')

    cfg = current_app.config
    recipient = email or cfg.get('MAIL_USERNAME') or cfg.get('MAIL_DEFAULT_SENDER')
    if not recipient:
        return jsonify({
            'ok': False,
            'error': '缺少收件人，请提供 email 或配置 MAIL_USERNAME/MAIL_DEFAULT_SENDER'
        }), 400

    from time import time
    from app.utils.helpers import send_email_with_result
    subject = 'SMTP 测试 - 鲲擎校园'
    body = f'这是一封 SMTP 测试邮件\n时间: {datetime.utcnow().isoformat()}'
    t0 = time()
    ok, err = send_email_with_result(recipient, subject, body)
    duration_ms = int((time() - t0) * 1000)

    details = {
        'server': cfg.get('MAIL_SERVER'),
        'port': int(cfg.get('MAIL_PORT') or 587),
        'use_tls': cfg.get('MAIL_USE_TLS', True),
        'use_ssl': cfg.get('MAIL_USE_SSL', False),
        'sender': cfg.get('MAIL_DEFAULT_SENDER') or cfg.get('MAIL_USERNAME'),
        'recipient': recipient,
        'duration_ms': duration_ms,
        'error': err,
    }

    return jsonify({'ok': ok, 'details': details})
