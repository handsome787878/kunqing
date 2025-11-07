from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..simple_models import SimpleStudyGroup
from ..utils.decorators import login_required


study_groups_bp = Blueprint("study_groups", __name__, url_prefix="/study_groups")


@study_groups_bp.route("/")
def index():
    groups = SimpleStudyGroup.get_all()
    return render_template("simple/study_groups_index.html", groups=groups)


@study_groups_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        title = data.get("title")
        subject = data.get("subject", "")
        goal = data.get("goal", "")
        target_members = int(data.get("target_members", 5))
        
        if not title:
            return jsonify({"error": "请填写小组标题"}), 400
        
        group = SimpleStudyGroup(current_user.id, title, subject, goal, target_members)
        
        if request.is_json:
            return jsonify({"message": "创建成功", "group_id": group.id})
        else:
            flash("创建成功！", "success")
            return redirect(url_for("study_groups.index"))
    
    return render_template("simple/study_groups_form.html")