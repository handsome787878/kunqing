"""通用辅助函数，包括图片处理、邮件发送、分页、搜索过滤和时间格式化等工具。"""

# 基础导入
import os
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional

from flask import current_app, request, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_mail import Message
from exts import mail

# 注释掉PIL导入，避免依赖问题
# from PIL import Image
# from sqlalchemy import and_, or_

import random
import string

_captcha_store = {}

# 允许的图片格式
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# 图片大小限制（字节）
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


# ==================== 验证码与邮件功能 ====================

def generate_captcha(length: int = 6) -> str:
    """生成数字验证码"""
    return "".join(random.choices(string.digits, k=length))


def store_captcha(email: str, code: str):
    """存储验证码（简单内存存储，生产环境建议使用Redis）"""
    _captcha_store[email] = code


def verify_captcha(email: str, code: str) -> bool:
    """验证验证码"""
    return _captcha_store.get(email) == code


def send_email(to_email: str, subject: str, body: str) -> bool:
    """使用 Flask-Mail 发送邮件，记录异常日志"""
    sender = current_app.config.get("MAIL_DEFAULT_SENDER") or current_app.config.get("MAIL_USERNAME")
    if not sender:
        current_app.logger.warning("邮件配置缺失：MAIL_DEFAULT_SENDER 或 MAIL_USERNAME 未设置")
        return False

    try:
        msg = Message(subject=subject, recipients=[to_email], body=body, sender=sender)
        mail.send(msg)
        return True
    except Exception:
        current_app.logger.exception("邮件发送失败（Flask-Mail）")
        return False


def send_email_with_result(to_email: str, subject: str, body: str):
    """发送邮件（测试用途），返回 (ok, error) 以便前端展示。
    不影响生产逻辑，尽量与 send_email 保持一致行为。
    """
    server = current_app.config.get("MAIL_SERVER")
    port = int(current_app.config.get("MAIL_PORT") or 587)
    username = current_app.config.get("MAIL_USERNAME")
    password = current_app.config.get("MAIL_PASSWORD")
    sender = current_app.config.get("MAIL_DEFAULT_SENDER") or username
    use_tls = current_app.config.get("MAIL_USE_TLS", True)
    use_ssl = current_app.config.get("MAIL_USE_SSL", False)

    if not server or not sender:
        current_app.logger.warning("邮件配置缺失：MAIL_SERVER 或 MAIL_DEFAULT_SENDER 未设置")
        return False, "MissingConfig(MAIL_SERVER/MAIL_DEFAULT_SENDER)"

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = to_email

    try:
        current_app.logger.info(
            f"准备发送测试邮件: server={server}, port={port}, use_ssl={use_ssl}, use_tls={use_tls}, sender={sender}, to={to_email}"
        )
        if use_ssl or port == 465:
            smtp = smtplib.SMTP_SSL(server, port)
        else:
            smtp = smtplib.SMTP(server, port)
            if use_tls:
                try:
                    smtp.starttls()
                except Exception:
                    current_app.logger.warning("SMTP starttls 失败，继续尝试登录发送")

        if username and password:
            smtp.login(username, password)
        smtp.sendmail(sender, [to_email], message.as_string())
        smtp.quit()
        return True, None
    except Exception as e:
        current_app.logger.exception("测试邮件发送失败")
        # 返回异常类型与消息，便于前端展示
        err = f"{e.__class__.__name__}: {str(e)}"
        return False, err


def send_verification_email(email: str) -> bool:
    """发送注册验证码邮件"""
    code = generate_captcha()
    store_captcha(email, code)
    
    subject = "鲲擎校园 - 注册验证码"
    body = f"""
    您好！
    
    您的注册验证码是：{code}
    
    验证码有效期为10分钟，请及时使用。
    
    如果这不是您的操作，请忽略此邮件。
    
    鲲擎校园团队
    """
    
    return send_email(email, subject, body)


def send_password_reset_email(email: str, reset_token: str) -> bool:
    """发送密码重置邮件"""
    reset_url = url_for('auth.reset_password', token=reset_token, _external=True)
    
    subject = "鲲擎校园 - 密码重置"
    body = f"""
    您好！
    
    您请求重置密码。请点击以下链接重置您的密码：
    
    {reset_url}
    
    此链接有效期为1小时。如果这不是您的操作，请忽略此邮件。
    
    鲲擎校园团队
    """
    
    return send_email(email, subject, body)


# 图片处理函数
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image_size(file) -> bool:
    """验证图片文件大小"""
    if hasattr(file, 'content_length') and file.content_length:
        return file.content_length <= MAX_FILE_SIZE
    
    # 如果无法获取content_length，读取文件检查大小
    file.seek(0, 2)  # 移动到文件末尾
    size = file.tell()
    file.seek(0)  # 重置文件指针
    return size <= MAX_FILE_SIZE


def save_uploaded_image(file, folder: str = 'images') -> Optional[str]:
    """保存上传的图片文件"""
    if not file or not allowed_file(file.filename):
        return None
    
    if not validate_image_size(file):
        return None
    
    # 生成唯一文件名
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    # 创建保存目录
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    save_dir = os.path.join(upload_folder, folder)
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(save_dir, unique_filename)
    file.save(file_path)
    
    return os.path.join(folder, unique_filename).replace('\\', '/')


def create_thumbnail(image_path: str, size: tuple = (200, 200)) -> Optional[str]:
    """创建图片缩略图（简化版本，不使用PIL）"""
    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        full_path = os.path.join(upload_folder, image_path)
        
        if not os.path.exists(full_path):
            return None
        
        # 简化实现：直接返回原图路径
        # 在生产环境中，建议使用专门的图片处理服务
        return image_path.replace('\\', '/')
    except Exception:
        return None


# 分页工具函数
class Pagination:
    """分页工具类"""
    
    def __init__(self, page: int, per_page: int, total: int, items: List[Any]):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items
        
    @property
    def pages(self) -> int:
        """总页数"""
        return (self.total - 1) // self.per_page + 1 if self.total > 0 else 1
    
    @property
    def has_prev(self) -> bool:
        """是否有上一页"""
        return self.page > 1
    
    @property
    def prev_num(self) -> Optional[int]:
        """上一页页码"""
        return self.page - 1 if self.has_prev else None
    
    @property
    def has_next(self) -> bool:
        """是否有下一页"""
        return self.page < self.pages
    
    @property
    def next_num(self) -> Optional[int]:
        """下一页页码"""
        return self.page + 1 if self.has_next else None
    
    def iter_pages(self, left_edge: int = 2, left_current: int = 2, 
                   right_current: int = 3, right_edge: int = 2) -> List[Optional[int]]:
        """生成分页页码列表"""
        last = self.pages
        for num in range(1, last + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > last - right_edge:
                yield num


def paginate_query(query, page: int, per_page: int = 20) -> Pagination:
    """对查询结果进行分页"""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return Pagination(page, per_page, total, items)


# 搜索过滤函数
def build_search_filter(model, search_fields: List[str], keyword: str):
    """构建搜索过滤条件"""
    if not keyword:
        return None
    
    filters = []
    for field in search_fields:
        if hasattr(model, field):
            attr = getattr(model, field)
            filters.append(attr.ilike(f'%{keyword}%'))
    
    return or_(*filters) if filters else None


def apply_filters(query, filters: Dict[str, Any]):
    """应用多个过滤条件"""
    for field, value in filters.items():
        if value is not None and value != '':
            if hasattr(query.column_descriptions[0]['type'], field):
                attr = getattr(query.column_descriptions[0]['type'], field)
                if isinstance(value, list):
                    query = query.filter(attr.in_(value))
                else:
                    query = query.filter(attr == value)
    return query


# 时间格式处理函数
def format_datetime(dt: datetime, format_type: str = 'default') -> str:
    """格式化日期时间"""
    if not dt:
        return ''
    
    now = datetime.now()
    diff = now - dt
    
    if format_type == 'relative':
        # 相对时间格式
        if diff.days > 0:
            return f"{diff.days}天前"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours}小时前"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes}分钟前"
        else:
            return "刚刚"
    elif format_type == 'date':
        return dt.strftime('%Y-%m-%d')
    elif format_type == 'datetime':
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # 默认格式：今天显示时间，其他显示日期
        if dt.date() == now.date():
            return dt.strftime('%H:%M')
        elif dt.year == now.year:
            return dt.strftime('%m-%d %H:%M')
        else:
            return dt.strftime('%Y-%m-%d')


def parse_datetime(date_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """解析日期时间字符串"""
    try:
        return datetime.strptime(date_str, format_str)
    except (ValueError, TypeError):
        return None


def get_date_range(range_type: str = 'week') -> tuple:
    """获取日期范围"""
    now = datetime.now()
    
    if range_type == 'today':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif range_type == 'week':
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
    elif range_type == 'month':
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end = now.replace(month=now.month + 1, day=1) - timedelta(microseconds=1)
    else:
        # 默认返回当天
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    return start, end


# ==================== 图片处理功能 ====================

def allowed_image_file(filename: str) -> bool:
    """检查文件是否为允许的图片格式"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def generate_unique_filename(filename: str) -> str:
    """生成唯一的文件名"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = str(uuid.uuid4())
    return f"{unique_name}.{ext}" if ext else unique_name


def save_image(file, upload_folder: str, max_size: Tuple[int, int] = (800, 600)) -> Optional[str]:
    """保存并处理图片"""
    if not file or not allowed_image_file(file.filename):
        return None
    
    # 检查文件大小
    file.seek(0, 2)  # 移动到文件末尾
    file_size = file.tell()
    file.seek(0)  # 重置到文件开头
    
    if file_size > MAX_IMAGE_SIZE:
        return None
    
    # 生成安全的文件名
    filename = generate_unique_filename(secure_filename(file.filename))
    filepath = os.path.join(upload_folder, filename)
    
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    
    try:
        # 直接保存文件，不使用PIL处理
        file.save(filepath)
        return filename
    except Exception:
        return None


def validate_image(file: FileStorage) -> bool:
    """验证上传的图片文件是否有效"""
    if not file or not file.filename:
        return False
    
    # 检查文件扩展名
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif'})
    if not ('.' in file.filename and 
            file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return False
    
    # 简化验证，不使用PIL
    return True


def delete_image(filename: str, upload_folder: str) -> bool:
    """删除图片文件"""
    if not filename:
        return True
    
    filepath = os.path.join(upload_folder, filename)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception:
        return False


# ==================== 分页功能 ====================

def get_pagination_info(page: int, per_page: int, total: int) -> Dict[str, Any]:
    """获取分页信息"""
    total_pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_num': page - 1 if has_prev else None,
        'next_num': page + 1 if has_next else None
    }


def paginate_query(query, page: int, per_page: int = 20):
    """对查询进行分页"""
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    pagination_info = get_pagination_info(page, per_page, total)
    
    return {
        'items': items,
        'pagination': pagination_info
    }


# ==================== 搜索过滤功能 ====================

def build_search_conditions(query_obj, search_params: Dict[str, Any]) -> Any:
    """构建搜索条件（简化版本，不使用SQLAlchemy）"""
    # 简化实现，返回原查询对象
    return query_obj


def build_search_filter(model, search_fields: List[str], search_term: str):
    """构建搜索过滤条件（简化版本）"""
    # 简化实现，不使用SQLAlchemy
    return None


def apply_filters(query_obj, filters: Dict[str, Any]) -> Any:
    """应用过滤条件（简化版本，不使用SQLAlchemy）"""
    # 简化实现，返回原查询对象
    return query_obj


def apply_filters_old(query, filters: Dict[str, Any]):
    """应用过滤条件（旧版本，简化）"""
    # 简化实现，不使用SQLAlchemy
    return query


# ==================== 时间格式化功能 ====================

def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """格式化日期时间"""
    if not dt:
        return ''
    return dt.strftime(format_str)


def format_date(dt: datetime, format_str: str = '%Y-%m-%d') -> str:
    """格式化日期"""
    return format_datetime(dt, format_str)


def time_ago(dt: datetime) -> str:
    """显示相对时间（多久之前）"""
    if not dt:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours}小时前'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes}分钟前'
    else:
        return '刚刚'


# ==================== URL和路径工具 ====================

def get_image_url(filename: str, folder: str = 'uploads') -> str:
    """获取图片URL"""
    if not filename:
        return url_for('static', filename='images/default-avatar.png')
    return url_for('static', filename=f'{folder}/{filename}')


def get_client_ip() -> str:
    """获取客户端IP地址"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


# ==================== 数据验证工具 ====================

def validate_email(email: str) -> bool:
    """简单的邮箱格式验证"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """简单的手机号格式验证（中国大陆）"""
    import re
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None


def sanitize_html(text: str) -> str:
    """清理HTML标签（简单实现）"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# ==================== 响应工具 ====================

def success_response(data: Any = None, message: str = '操作成功') -> Dict[str, Any]:
    """成功响应格式"""
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return response


def error_response(message: str = '操作失败', code: int = 400) -> Dict[str, Any]:
    """错误响应格式"""
    return {
        'success': False,
        'message': message,
        'code': code
    }
