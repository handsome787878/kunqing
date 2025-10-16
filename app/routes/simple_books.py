from flask import Blueprint, request, render_template_string, redirect, url_for, flash, jsonify

from flask_login import current_user

from ..simple_models import SimpleBook
from ..utils.decorators import login_required


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/")
def index():
    books = SimpleBook.get_all()
    
    books_html = ""
    for book in books:
        status_class = "status-active" if book.status == "available" else "status-sold"
        status_text = "在售" if book.status == "available" else "已售"
        
        books_html += f"""
        <div class="card">
            <div class="card-header">
                <h3>📚 {book.book_name}</h3>
                <span class="badge {status_class}">{status_text}</span>
            </div>
            <div class="card-content">
                <p><strong>作者:</strong> {book.author}</p>
                <p><strong>价格:</strong> <span style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">¥{book.price}</span></p>
                <p><strong>成色:</strong> {book.condition}</p>
                <p><strong>描述:</strong> {book.description}</p>
                <p><strong>发布时间:</strong> {book.create_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        """
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>二手书交易 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
        <style>
            .badge {{
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8em;
                font-weight: bold;
            }}
            .status-active {{
                background-color: #28a745;
                color: white;
            }}
            .status-sold {{
                background-color: #dc3545;
                color: white;
            }}
            .card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .card-header h3 {{
                margin: 0;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h2>📚 二手书交易</h2>
                <p>买卖二手教材，节约成本，环保生活</p>
                
                <div style="text-align: center; margin-bottom: 30px;">
                    <a href="{{{{ url_for('books.create') }}}}" class="btn">📖 发布二手书</a>
                </div>
                
                <div class="cards-grid">
                    {books_html if books_html else '<div class="card"><div class="card-content"><p>暂无二手书信息</p></div></div>'}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{{{{ url_for('index') }}}}" class="back-link">← 返回首页</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


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
    
    return render_template_string("""
    <h2>发布二手书</h2>
    <form method="POST">
        <p>
            <label>书名:</label><br>
            <input type="text" name="book_name" required>
        </p>
        <p>
            <label>作者:</label><br>
            <input type="text" name="author">
        </p>
        <p>
            <label>价格:</label><br>
            <input type="number" name="price" step="0.01" min="0">
        </p>
        <p>
            <label>成色:</label><br>
            <select name="condition">
                <option value="">请选择</option>
                <option value="全新">全新</option>
                <option value="九成新">九成新</option>
                <option value="八成新">八成新</option>
                <option value="七成新">七成新</option>
                <option value="其他">其他</option>
            </select>
        </p>
        <p>
            <label>描述:</label><br>
            <textarea name="description" rows="4" cols="50"></textarea>
        </p>
        <p>
            <input type="submit" value="发布">
        </p>
    </form>
    <a href="{{ url_for('books.index') }}">返回列表</a>
    """)