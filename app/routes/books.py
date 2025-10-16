from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from ..models import db, SecondhandBook, BookMessage
from ..utils.decorators import login_required


books_bp = Blueprint("books", __name__, url_prefix="/books")


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", set())


def save_images(files, subdir: str = "books"):
    saved = []
    base_upload = current_app.config.get("UPLOAD_FOLDER")
    target_dir = os.path.join(base_upload, subdir)
    os.makedirs(target_dir, exist_ok=True)
    for f in files:
        if f and f.filename and allowed_file(f.filename):
            fname = datetime.utcnow().strftime("%Y%m%d%H%M%S%f_") + secure_filename(f.filename)
            path = os.path.join(target_dir, fname)
            f.save(path)
            rel_url = "/static/images/uploads/" + f"{subdir}/" + fname
            saved.append(rel_url)
    return saved


@books_bp.route("/", methods=["GET"])
def list_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))
    q = request.args.get("q", "").strip()
    course = request.args.get("course")
    college = request.args.get("college")
    status = request.args.get("status")
    sort = request.args.get("sort", "time_desc")

    query = SecondhandBook.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(SecondhandBook.book_name.ilike(like), SecondhandBook.description.ilike(like)))
    if course:
        query = query.filter(SecondhandBook.course == course)
    if college:
        query = query.filter(SecondhandBook.college == college)
    if status:
        query = query.filter(SecondhandBook.status == status)
    if sort == "price_asc":
        query = query.order_by(SecondhandBook.price.asc())
    elif sort == "price_desc":
        query = query.order_by(SecondhandBook.price.desc())
    else:
        query = query.order_by(SecondhandBook.create_time.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("books/book_list.html", books=pagination.items, pagination=pagination, q=q, course=course, college=college, status=status, sort=sort)


@books_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_book():
    if request.method == "POST":
        book_name = request.form.get("book_name", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        publisher = request.form.get("publisher", "").strip()
        course = request.form.get("course", "").strip()
        college = request.form.get("college", "").strip()
        price_str = request.form.get("price", "").strip()
        condition = request.form.get("condition", "").strip()
        description = request.form.get("description", "").strip()
        files = request.files.getlist("images")

        if not book_name:
            flash("书名必填", "danger")
            return redirect(url_for("books.create_book"))
        try:
            price = float(price_str) if price_str else 0
            if price < 0:
                raise ValueError
        except ValueError:
            flash("价格格式不正确", "danger")
            return redirect(url_for("books.create_book"))

        allowed_conditions = {"new", "like_new", "good", "fair", "poor"}
        if condition and condition not in allowed_conditions:
            flash("成色选择不合法", "danger")
            return redirect(url_for("books.create_book"))

        images = save_images(files, subdir="books")
        book = SecondhandBook(
            user_id=current_user.id,
            book_name=book_name,
            author=author,
            isbn=isbn,
            publisher=publisher,
            course=course,
            college=college,
            price=price,
            condition=condition or None,
            description=description,
            images=images,
        )
        db.session.add(book)
        db.session.commit()
        flash("发布成功", "success")
        return redirect(url_for("books.detail", book_id=book.id))

    return render_template("books/book_form.html")


@books_bp.route("/<int:book_id>", methods=["GET"])
def detail(book_id: int):
    book = db.session.get(SecondhandBook, book_id)
    if not book:
        return "Not Found", 404
    messages = BookMessage.query.filter_by(book_id=book.id).order_by(BookMessage.create_time.desc()).all()
    return render_template("books/book_detail.html", book=book, messages=messages)


@books_bp.route("/<int:book_id>/status", methods=["POST"])
@login_required
def update_status(book_id: int):
    book = db.session.get(SecondhandBook, book_id)
    if not book:
        return jsonify({"error": "not_found"}), 404
    if book.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403
    status = request.form.get("status")
    if status not in ("available", "reserved", "sold"):
        return jsonify({"error": "bad_status"}), 400
    book.status = status
    db.session.commit()
    return jsonify({"ok": True, "status": book.status})


@books_bp.route("/<int:book_id>/messages", methods=["GET", "POST"])
def book_messages(book_id: int):
    book = db.session.get(SecondhandBook, book_id)
    if not book:
        return jsonify({"error": "not_found"}), 404
    if request.method == "POST":
        if not current_user.is_authenticated:
            return jsonify({"error": "auth_required"}), 401
        content = request.form.get("content", "").strip()
        if not content:
            return jsonify({"error": "empty"}), 400
        msg = BookMessage(book_id=book.id, user_id=current_user.id, content=content)
        db.session.add(msg)
        db.session.commit()
        # 可选：通知书主，这里略过
        return jsonify({"ok": True, "message": {"id": msg.id, "content": msg.content, "user_id": msg.user_id, "create_time": msg.create_time.isoformat()}})
    # GET 列表
    items = BookMessage.query.filter_by(book_id=book.id).order_by(BookMessage.create_time.desc()).all()
    return jsonify({"messages": [{"id": m.id, "user_id": m.user_id, "content": m.content, "create_time": m.create_time.isoformat()} for m in items]})


@books_bp.route("/mine", methods=["GET"])
@login_required
def my_books():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))
    query = SecondhandBook.query.filter_by(user_id=current_user.id).order_by(SecondhandBook.create_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("books/book_list.html", books=pagination.items, pagination=pagination, mine=True)


@books_bp.route("/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id: int):
    book = db.session.get(SecondhandBook, book_id)
    if not book:
        return "Not Found", 404
    if book.user_id != current_user.id:
        return "Forbidden", 403
    if request.method == "POST":
        book_name = request.form.get("book_name", "").strip()
        if book_name:
            book.book_name = book_name
        for field in ["author", "isbn", "publisher", "course", "college", "description"]:
            val = request.form.get(field)
            if val is not None:
                setattr(book, field, val)
        price_str = request.form.get("price")
        if price_str is not None:
            try:
                price = float(price_str)
                if price < 0:
                    raise ValueError
                book.price = price
            except ValueError:
                flash("价格格式不正确", "danger")
                return redirect(url_for("books.edit_book", book_id=book.id))
        condition = request.form.get("condition")
        allowed_conditions = {"new", "like_new", "good", "fair", "poor"}
        if condition and condition not in allowed_conditions:
            flash("成色选择不合法", "danger")
            return redirect(url_for("books.edit_book", book_id=book.id))
        files = request.files.getlist("images")
        new_images = save_images(files, subdir="books")
        if new_images:
            book.images = (book.images or []) + new_images
        db.session.commit()
        flash("已更新", "success")
        return redirect(url_for("books.detail", book_id=book.id))
    return render_template("books/book_form.html", book=book)


@books_bp.route("/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id: int):
    book = db.session.get(SecondhandBook, book_id)
    if not book:
        return "Not Found", 404
    if book.user_id != current_user.id:
        return "Forbidden", 403
    db.session.delete(book)
    db.session.commit()
    flash("已删除", "success")
    return redirect(url_for("books.my_books"))