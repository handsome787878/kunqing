from flask import Blueprint, request, render_template_string, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..simple_models import SimpleStudyGroup
from ..utils.decorators import login_required


study_groups_bp = Blueprint("study_groups", __name__, url_prefix="/study_groups")


@study_groups_bp.route("/")
def index():
    groups = SimpleStudyGroup.get_all()
    
    groups_html = ""
    for group in groups:
        status_class = "status-open" if group.status == "open" else "status-closed"
        groups_html += f"""
        <div class="study-group-card">
            <h3 class="group-title">{group.title}</h3>
            <div class="group-meta">
                <span class="meta-item">📖 {group.subject or '未指定学科'}</span>
                <span class="meta-item">🎯 {group.goal or '暂无目标描述'}</span>
                <span class="meta-item">👥 {group.current_members}/{group.target_members}人</span>
                <span class="meta-item {status_class}">
                    {'🟢 开放加入' if group.status == 'open' else '🔴 已关闭'}
                </span>
                <span class="meta-item">📅 {group.create_time.strftime('%Y-%m-%d')}</span>
            </div>
        </div>
        """
    
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>学习小组 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
        <style>
            .study-group-card {{
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 15px 0;
                padding: 20px;
                transition: transform 0.2s;
            }}
            .study-group-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }}
            .group-title {{
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 1.3em;
            }}
            .group-meta {{
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                margin-top: 10px;
            }}
            .meta-item {{
                background: #f8f9fa;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 0.9em;
            }}
            .status-open {{
                background: #d4edda;
                color: #155724;
            }}
            .status-closed {{
                background: #f8d7da;
                color: #721c24;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h1>📚 学习小组</h1>
                <p>加入学习小组，与志同道合的同学一起学习进步！</p>
                
                <div class="action-buttons">
                    <a href="{{{{ url_for('study_groups.create') }}}}" class="btn btn-primary">创建学习小组</a>
                </div>
                
                <div class="study-groups-list">
                    {groups_html if groups_html else '<div class="empty-state"><p>暂无学习小组，快来创建第一个吧！</p></div>'}
                </div>
                
                <div class="navigation">
                    <a href="{{{{ url_for('index') }}}}" class="btn btn-secondary">返回首页</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


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
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>创建学习小组 - 鲲擎校园</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    </head>
    <body>
        <div class="container">
            <div class="main-content">
                <h1>📝 创建学习小组</h1>
                <p>创建一个学习小组，邀请志同道合的同学一起学习！</p>
                
                <div class="form-container">
                    <form method="POST">
                        <div class="form-group">
                            <label for="title">小组标题 *</label>
                            <input type="text" id="title" name="title" required placeholder="请输入小组标题">
                        </div>
                        
                        <div class="form-group">
                            <label for="subject">学科</label>
                            <input type="text" id="subject" name="subject" placeholder="如：数学、英语、计算机等">
                        </div>
                        
                        <div class="form-group">
                            <label for="goal">学习目标</label>
                            <textarea id="goal" name="goal" rows="4" placeholder="描述一下这个学习小组的目标和计划..."></textarea>
                        </div>
                        
                        <div class="form-group">
                            <label for="target_members">目标成员数</label>
                            <input type="number" id="target_members" name="target_members" value="5" min="2" max="20">
                            <small>建议2-20人，便于有效交流</small>
                        </div>
                        
                        <div class="form-actions">
                            <button type="submit" class="btn btn-primary">创建小组</button>
                            <a href="{{ url_for('study_groups.index') }}" class="btn btn-secondary">取消</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)