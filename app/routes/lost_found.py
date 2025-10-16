from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from ..models import db, LostFound
from ..utils.decorators import login_required


lf_bp = Blueprint("lost_found", __name__, url_prefix="/lost-found")


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", set())


def save_images(files, subdir: str = "lost_found"):
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


@lf_bp.route("/", methods=["GET"])
def list_items():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))
    q = request.args.get("q", "").strip()
    type_ = request.args.get("type")
    category = request.args.get("category")
    status = request.args.get("status")

    query = LostFound.query
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(LostFound.title.ilike(like), LostFound.description.ilike(like)))
    if type_:
        query = query.filter(LostFound.type == type_)
    if category:
        query = query.filter(LostFound.category == category)
    if status:
        query = query.filter(LostFound.status == status)

    query = query.order_by(LostFound.create_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    return render_template(
        "lost_found/lost_found_list.html",
        items=items,
        pagination=pagination,
        q=q,
        type=type_,
        category=category,
        status=status,
    )


@lf_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_item():
    if request.method == "POST":
        type_ = request.form.get("type")
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        lost_time_str = request.form.get("lost_time")
        contact = request.form.get("contact", "").strip()
        files = request.files.getlist("images")

        if type_ not in ("lost", "found"):
            flash("类型不合法", "danger")
            return redirect(url_for("lost_found.create_item"))
        if not title:
            flash("标题必填", "danger")
            return redirect(url_for("lost_found.create_item"))

        lost_time = None
        if lost_time_str:
            try:
                lost_time = datetime.fromisoformat(lost_time_str)
            except ValueError:
                flash("时间格式不正确", "danger")
                return redirect(url_for("lost_found.create_item"))

        image_paths = save_images(files, subdir="lost_found")
        item = LostFound(
            user_id=current_user.id,
            type=type_,
            title=title,
            category=category,
            description=description,
            location=location,
            lost_time=lost_time,
            contact=contact,
            images=image_paths,
        )
        db.session.add(item)
        db.session.commit()
        flash("发布成功", "success")
        return redirect(url_for("lost_found.detail", item_id=item.id))

    return render_template("lost_found/lost_found_form.html")


@lf_bp.route("/<int:item_id>", methods=["GET"])
def detail(item_id: int):
    item = db.session.get(LostFound, item_id)
    if not item:
        return "Not Found", 404
    return render_template("lost_found/lost_found_detail.html", item=item)


@lf_bp.route("/<int:item_id>/status", methods=["POST"])
@login_required
def update_status(item_id: int):
    item = db.session.get(LostFound, item_id)
    if not item:
        return jsonify({"error": "not_found"}), 404
    if item.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403
    status = request.form.get("status")
    if status not in ("open", "found", "returned"):
        return jsonify({"error": "bad_status"}), 400
    item.status = status
    db.session.commit()
    return jsonify({"ok": True, "status": item.status})


@lf_bp.route("/mine", methods=["GET"])
@login_required
def my_items():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))
    query = LostFound.query.filter_by(user_id=current_user.id).order_by(LostFound.create_time.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("lost_found/lost_found_list.html", items=pagination.items, pagination=pagination, mine=True)


@lf_bp.route("/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id: int):
    item = db.session.get(LostFound, item_id)
    if not item:
        return "Not Found", 404
    if item.user_id != current_user.id:
        return "Forbidden", 403

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        if title:
            item.title = title
        category = request.form.get("category")
        if category is not None:
            item.category = category
        description = request.form.get("description")
        if description is not None:
            item.description = description
        location = request.form.get("location")
        if location is not None:
            item.location = location
        contact = request.form.get("contact")
        if contact is not None:
            item.contact = contact

        files = request.files.getlist("images")
        new_images = save_images(files, subdir="lost_found")
        if new_images:
            item.images = (item.images or []) + new_images

        db.session.commit()
        flash("已更新", "success")
        return redirect(url_for("lost_found.detail", item_id=item.id))

    return render_template("lost_found/lost_found_form.html", item=item)


@lf_bp.route("/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id: int):
    item = db.session.get(LostFound, item_id)
    if not item:
        return "Not Found", 404
    if item.user_id != current_user.id:
        return "Forbidden", 403
    db.session.delete(item)
    db.session.commit()
    flash("已删除", "success")
    return redirect(url_for("lost_found.my_items"))