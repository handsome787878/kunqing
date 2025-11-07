"""学校选择与搜索路由"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.models import db, School

school_bp = Blueprint("school", __name__, url_prefix="/school")


@school_bp.route("/select")
def select():
    """学校选择页面"""
    # 初始加载显示前若干学校
    schools = School.query.order_by(School.name.asc()).limit(50).all()
    return render_template("school/select.html", schools=schools)


@school_bp.route("/search")
def search():
    """按名称模糊搜索学校，返回JSON"""
    q = (request.args.get("q") or "").strip()
    query = School.query
    if q:
        like = f"%{q}%"
        query = query.filter(School.name.ilike(like))
    results = query.order_by(School.name.asc()).limit(50).all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "province": s.province,
            "city": s.city,
        }
        for s in results
    ])


@school_bp.route("/set/<int:school_id>")
def set_current_school(school_id: int):
    """设置当前选择的学校到会话并返回主页"""
    school = School.query.get(school_id)
    if not school:
        flash("学校不存在", "error")
        return redirect(url_for("school.select"))
    session["current_school_id"] = school.id
    flash(f"已切换学校：{school.name}", "success")
    return redirect(url_for("index"))