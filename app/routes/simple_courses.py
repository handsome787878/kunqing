from flask import Blueprint, request, render_template_string, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..simple_models import SimpleCourse
from ..utils.decorators import login_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
def index():
    courses = SimpleCourse.get_all()
    
    courses_html = ""
    for course in courses:
        courses_html += f"""
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h3>{course.course_name}</h3>
            <p><strong>课程代码:</strong> {course.course_code}</p>
            <p><strong>教师:</strong> {course.teacher}</p>
            <p><strong>学院:</strong> {course.college}</p>
            <p><strong>描述:</strong> {course.description}</p>
        </div>
        """
    
    return render_template_string(f"""
    <h2>课程评价</h2>
    <p><a href="{{{{ url_for('courses.create') }}}}">添加课程</a></p>
    <div>
        {courses_html if courses_html else '<p>暂无课程信息</p>'}
    </div>
    <a href="{{{{ url_for('index') }}}}">返回首页</a>
    """)


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
    
    return render_template_string("""
    <h2>添加课程</h2>
    <form method="POST">
        <p>
            <label>课程代码:</label><br>
            <input type="text" name="course_code" required>
        </p>
        <p>
            <label>课程名称:</label><br>
            <input type="text" name="course_name" required>
        </p>
        <p>
            <label>教师:</label><br>
            <input type="text" name="teacher">
        </p>
        <p>
            <label>学院:</label><br>
            <input type="text" name="college">
        </p>
        <p>
            <input type="submit" value="添加">
        </p>
    </form>
    <a href="{{ url_for('courses.index') }}">返回列表</a>
    """)