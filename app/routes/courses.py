from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..models import db, Course, CourseReview
from ..utils.decorators import login_required


courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/", methods=["GET"])
def list_courses():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 12))
    q = request.args.get("q", "").strip()
    teacher = request.args.get("teacher")
    college = request.args.get("college")

    query = Course.query
    if q:
        like = f"%{q}%"
        query = query.filter(Course.course_name.ilike(like))
    if teacher:
        query = query.filter(Course.teacher == teacher)
    if college:
        query = query.filter(Course.college == college)

    query = query.order_by(Course.course_name.asc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("courses/course_list.html", courses=pagination.items, pagination=pagination, q=q, teacher=teacher, college=college)


@courses_bp.route("/<int:course_id>", methods=["GET"])
def detail(course_id: int):
    course = db.session.get(Course, course_id)
    if not course:
        return "Not Found", 404
    # 评价统计
    reviews_query = CourseReview.query.filter_by(course_id=course.id)
    count = reviews_query.count()
    avg_rating = avg_diff = avg_work = None
    if count:
        from sqlalchemy import func

        avg_rating = db.session.query(func.avg(CourseReview.rating)).filter_by(course_id=course.id).scalar()
        avg_diff = db.session.query(func.avg(CourseReview.difficulty)).filter_by(course_id=course.id).scalar()
        avg_work = db.session.query(func.avg(CourseReview.workload)).filter_by(course_id=course.id).scalar()

    # 评价列表分页
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    pagination = reviews_query.order_by(CourseReview.create_time.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template(
        "courses/course_detail.html",
        course=course,
        pagination=pagination,
        reviews=pagination.items,
        avg_rating=avg_rating,
        avg_diff=avg_diff,
        avg_work=avg_work,
        count=count,
    )


@courses_bp.route("/<int:course_id>/review", methods=["GET", "POST"])
@login_required
def publish_review(course_id: int):
    course = db.session.get(Course, course_id)
    if not course:
        return "Not Found", 404
    if request.method == "POST":
        def parse_int(name):
            try:
                return int(request.form.get(name, 0))
            except (TypeError, ValueError):
                return 0

        rating = parse_int("rating")
        difficulty = parse_int("difficulty")
        workload = parse_int("workload")
        content = request.form.get("content", "").strip()
        exam_info = request.form.get("exam_info", "").strip()
        study_tips = request.form.get("study_tips", "").strip()
        is_anonymous = request.form.get("is_anonymous") in ("on", "true", "1")

        if not (1 <= rating <= 5):
            flash("综合评分需在 1-5", "danger")
            return redirect(url_for("courses.publish_review", course_id=course.id))

        review = CourseReview(
            course_id=course.id,
            user_id=current_user.id,
            rating=rating,
            difficulty=difficulty,
            workload=workload,
            content=content,
            exam_info=exam_info,
            study_tips=study_tips,
            is_anonymous=is_anonymous,
        )
        db.session.add(review)
        db.session.commit()
        flash("评价已发布", "success")
        return redirect(url_for("courses.detail", course_id=course.id))

    return render_template("courses/review_form.html", course=course)


@courses_bp.route("/my-reviews", methods=["GET"])
@login_required
def my_reviews():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    query = CourseReview.query.filter_by(user_id=current_user.id).order_by(CourseReview.create_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("courses/my_reviews.html", reviews=pagination.items, pagination=pagination)


@courses_bp.route("/<int:review_id>/edit", methods=["GET", "POST"])
@login_required
def edit_review(review_id: int):
    review = db.session.get(CourseReview, review_id)
    if not review:
        return "Not Found", 404
    if review.user_id != current_user.id:
        return "Forbidden", 403
    if request.method == "POST":
        for field in ["content", "exam_info", "study_tips"]:
            val = request.form.get(field)
            if val is not None:
                setattr(review, field, val)
        def parse_int(name):
            try:
                return int(request.form.get(name, 0))
            except (TypeError, ValueError):
                return 0
        rating = parse_int("rating")
        difficulty = parse_int("difficulty")
        workload = parse_int("workload")
        if rating:
            review.rating = rating
        if difficulty:
            review.difficulty = difficulty
        if workload:
            review.workload = workload
        review.is_anonymous = request.form.get("is_anonymous") in ("on", "true", "1")
        db.session.commit()
        flash("评价已更新", "success")
        return redirect(url_for("courses.detail", course_id=review.course_id))
    return render_template("courses/review_form.html", review=review, course=review.course)