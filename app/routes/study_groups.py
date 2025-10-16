from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user
from datetime import datetime

from ..models import db, StudyGroup, GroupMember
from ..utils.decorators import login_required


sg_bp = Blueprint("study_groups", __name__, url_prefix="/study-groups")


@sg_bp.route("/", methods=["GET"])
def list_groups():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 12))
    q = request.args.get("q", "").strip()
    subject = request.args.get("subject")
    status = request.args.get("status")

    query = StudyGroup.query
    if q:
        like = f"%{q}%"
        query = query.filter(StudyGroup.title.ilike(like))
    if subject:
        query = query.filter(StudyGroup.subject == subject)
    if status:
        query = query.filter(StudyGroup.status == status)

    query = query.order_by(StudyGroup.create_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("study_groups/group_list.html", groups=pagination.items, pagination=pagination, q=q, subject=subject, status=status)


@sg_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        goal = request.form.get("goal", "").strip()
        plan = request.form.get("plan", "").strip()
        requirements = request.form.get("requirements", "").strip()
        target_members = request.form.get("target_members")
        deadline_str = request.form.get("deadline")

        if not title:
            flash("标题必填", "danger")
            return redirect(url_for("study_groups.create_group"))

        try:
            target_members = int(target_members) if target_members else None
        except ValueError:
            flash("目标人数需为整数", "danger")
            return redirect(url_for("study_groups.create_group"))

        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                flash("截止时间格式错误，需为 YYYY-MM-DD", "danger")
                return redirect(url_for("study_groups.create_group"))

        group = StudyGroup(
            user_id=current_user.id,
            title=title,
            subject=subject or None,
            goal=goal or None,
            plan=plan or None,
            requirements=requirements or None,
            target_members=target_members,
            deadline=deadline,
        )
        db.session.add(group)
        db.session.commit()
        # 创建者加入成员列表为 owner
        db.session.add(GroupMember(group_id=group.id, user_id=current_user.id, role="owner"))
        db.session.commit()
        flash("小组已创建", "success")
        return redirect(url_for("study_groups.detail", group_id=group.id))

    return render_template("study_groups/group_form.html")


@sg_bp.route("/<int:group_id>", methods=["GET"])
def detail(group_id: int):
    group = db.session.get(StudyGroup, group_id)
    if not group:
        return "Not Found", 404
    members = GroupMember.query.filter_by(group_id=group.id).order_by(GroupMember.join_time.asc()).all()
    return render_template("study_groups/group_detail.html", group=group, members=members)


@sg_bp.route("/<int:group_id>/apply", methods=["GET", "POST"])
@login_required
def apply(group_id: int):
    group = db.session.get(StudyGroup, group_id)
    if not group:
        return "Not Found", 404
    if request.method == "POST":
        # 简化：直接加入，真实场景应有审核流程
        if GroupMember.query.filter_by(group_id=group.id, user_id=current_user.id).first():
            flash("已在小组中", "info")
            return redirect(url_for("study_groups.detail", group_id=group.id))
        if group.status == "closed":
            flash("小组已满员或关闭", "warning")
            return redirect(url_for("study_groups.detail", group_id=group.id))
        db.session.add(GroupMember(group_id=group.id, user_id=current_user.id, role="member"))
        group.current_members = (group.current_members or 0) + 1
        # 满员自动关闭
        if group.target_members and group.current_members >= group.target_members:
            group.status = "closed"
        db.session.commit()
        flash("申请已加入", "success")
        return redirect(url_for("study_groups.detail", group_id=group.id))
    return render_template("study_groups/group_application.html", group=group)


@sg_bp.route("/<int:group_id>/manage", methods=["GET", "POST"])
@login_required
def manage(group_id: int):
    group = db.session.get(StudyGroup, group_id)
    if not group:
        return "Not Found", 404
    if group.user_id != current_user.id:
        return "Forbidden", 403
    if request.method == "POST":
        status = request.form.get("status")
        if status in ("open", "closed"):
            group.status = status
            db.session.commit()
            flash("状态已更新", "success")
        return redirect(url_for("study_groups.manage", group_id=group.id))
    members = GroupMember.query.filter_by(group_id=group.id).order_by(GroupMember.join_time.asc()).all()
    return render_template("study_groups/group_manage.html", group=group, members=members)