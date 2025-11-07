from flask import Blueprint, request, render_template, render_template_string, redirect, url_for, flash, jsonify

from flask_login import current_user

from ..simple_models import SimpleBook
from ..utils.decorators import login_required


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/")
def index():
    books = SimpleBook.get_all()
    return render_template("simple/books_index.html", books=books)


@books_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        book_name = data.get("book_name")
        author = data.get("author", "")
        price = float(data.get("price", 0))
        condition = data.get("condition", "")
        description = data.get("description", "")
        
        if not book_name:
            return jsonify({"error": "请填写书名"}), 400
        
        book = SimpleBook(current_user.id, book_name, author, price, condition, description)
        
        if request.is_json:
            return jsonify({"message": "发布成功", "book_id": book.id})
        else:
            flash("发布成功！", "success")
            return redirect(url_for("books.index"))
    
    return render_template("simple/books_form.html")