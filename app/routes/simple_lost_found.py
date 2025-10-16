from flask import Blueprint, request, render_template_string, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..simple_models import SimpleLostFound
from ..utils.decorators import login_required


lost_found_bp = Blueprint("lost_found", __name__, url_prefix="/lost_found")


@lost_found_bp.route("/")
def index():
    items = SimpleLostFound.get_all()
    
    items_html = ""
    
    for item in items:
        status_class = "status-active" if item.status == "active" else "status-resolved"
        type_emoji = "🔍" if item.type == "lost" else "📦"
        type_text = "失物" if item.type == "lost" else "招领"
        
        items_html += f"""
        <div class="card">
            <div class="card-header">
                <h3>{type_emoji} {item.title}</h3>
                <span class="badge {status_class}">{item.status}</span>
            </div>
            <div class="card-content">
                <p><strong>类型:</strong> {type_text}</p>
                <p><strong>描述:</strong> {item.description}</p>
                <p><strong>地点:</strong> {item.location}</p>
                <p><strong>联系方式:</strong> {item.contact}</p>
                <p><strong>发布时间:</strong> {item.create_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
        """
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>失物招领 - 鲲擎校园</title>
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
            .status-resolved {{
                background-color: #6c757d;
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
                <h2>🔍 失物招领</h2>
                <p>帮助同学们找回丢失的物品，传递校园温暖</p>
                
                <div style="text-align: center; margin-bottom: 30px;">
                    <a href="{{{{ url_for('lost_found.create') }}}}" class="btn">📝 发布失物招领</a>
                </div>
                
                <div class="cards-grid">
                    {items_html if items_html else '<div class="card"><div class="card-content"><p>暂无失物招领信息</p></div></div>'}
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{{{{ url_for('index') }}}}" class="back-link">← 返回首页</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@lost_found_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = request.get_json() if request.is_json else request.form
        
        type = data.get("type")
        title = data.get("title")
        description = data.get("description", "")
        location = data.get("location", "")
        contact = data.get("contact", "")
        
        if not all([type, title]):
            return jsonify({"error": "请填写必填字段"}), 400
        
        item = SimpleLostFound(current_user.id, type, title, description, location, contact)
        
        if request.is_json:
            return jsonify({"message": "发布成功", "item_id": item.id})
        else:
            flash("发布成功！", "success")
            return redirect(url_for("lost_found.index"))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>发布失物招领 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h2>📝 发布失物招领</h2>
                <p>帮助同学们找回丢失的物品，或者发布拾到的物品信息</p>
                
                <div class="form-container">
                    <form method="POST">
                        <div class="form-group">
                            <label for="type">类型 *</label>
                            <select id="type" name="type" required>
                                <option value="">请选择类型</option>
                                <option value="lost">🔍 失物 - 我丢失了物品</option>
                                <option value="found">📦 招领 - 我拾到了物品</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="title">标题 *</label>
                            <input type="text" id="title" name="title" required placeholder="请简要描述物品">
                        </div>
                        
                        <div class="form-group">
                            <label for="description">详细描述</label>
                            <textarea id="description" name="description" rows="4" placeholder="请详细描述物品的特征、颜色、大小等信息"></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="location">相关地点</label>
                            <input type="text" id="location" name="location" placeholder="丢失地点或拾到地点">
                        </div>
                        
                        <div class="form-group">
                            <label for="contact">联系方式</label>
                            <input type="text" id="contact" name="contact" placeholder="QQ、微信、电话等联系方式">
                        </div>
                        
                        <div class="form-group" style="text-align: center;">
                            <button type="submit" class="btn">发布信息</button>
                        </div>
                    </form>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{{ url_for('lost_found.index') }}" class="back-link">← 返回失物招领</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)