from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from flask_login import current_user

from ..simple_models import SimpleLostFound
from ..models import db, School
from ..utils.decorators import login_required


lost_found_bp = Blueprint("lost_found", __name__, url_prefix="/lost_found")


@lost_found_bp.route("/")
def index():
    scope = (request.args.get("scope") or "").strip()
    sid = session.get("current_school_id")
    items = []
    if scope == "all":
        items = SimpleLostFound.get_all_public()
    else:
        if not sid:
            flash("请选择所在学校以查看本校失物信息", "info")
        else:
            items = SimpleLostFound.get_by_school(sid)
    return render_template("simple/lost_found_index.html", items=items, scope=scope)


@lost_found_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        type = data.get("type")
        title = data.get("title")
        description = data.get("description", "")
        location = data.get("location", "")
        contact = data.get("contact", "")
        is_public = bool(data.get("is_public"))
        sid = session.get("current_school_id")
        school_id = data.get("school_id")
        
        # 选择学校策略：普通用户使用当前学校；管理员可选择学校
        if current_user.can_manage_content() and school_id:
            try:
                school_id = int(school_id)
            except Exception:
                school_id = None
        else:
            school_id = sid
        
        # 获取学校名称用于展示
        school_name = None
        if school_id:
            s = School.query.get(int(school_id))
            school_name = s.name if s else None
        
        if not school_id:
            msg = "请先选择所在学校后再发布信息"
            if request.is_json:
                return jsonify({"error": msg}), 400
            flash(msg, "warning")
            return redirect(url_for("school.select"))
        
        if not all([type, title]):
            return jsonify({"error": "请填写必填字段"}), 400
        
        item = SimpleLostFound(current_user.id, type, title, description, location, contact, school_id=school_id, school_name=school_name, is_public=is_public)
        
        if request.is_json:
            return jsonify({"message": "发布成功", "item_id": item.id})
        else:
            flash("发布成功！", "success")
            return redirect(url_for("lost_found.index"))
    
    # GET：渲染表单，管理员支持选择学校
    schools = []
    if hasattr(current_user, "can_manage_content") and current_user.can_manage_content():
        schools = School.query.order_by(School.name.asc()).limit(200).all()
    return render_template("simple/lost_found_form.html", schools=schools)