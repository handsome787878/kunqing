from flask import Blueprint, request, render_template, render_template_string, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..simple_models import SimpleCourse
from ..utils.decorators import login_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
def index():
    courses = SimpleCourse.get_all()
    return render_template("simple/courses_index.html", courses=courses)


@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        course_code = data.get("course_code")
        course_name = data.get("course_name")
        teacher = data.get("teacher", "")
        college = data.get("college", "")
        
        if not all([course_code, course_name]):
            return jsonify({"error": "请填写课程代码和课程名称"}), 400
        
        course = SimpleCourse(course_code, course_name, teacher, college)
        
        if request.is_json:
            return jsonify({"message": "添加成功", "course_id": course.id})
        else:
            flash("添加成功！", "success")
            return redirect(url_for("courses.index"))
    
    return render_template("simple/courses_form.html")