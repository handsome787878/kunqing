# 鲲擎校园系统 🎓

一个基于Flask的校园综合服务平台，提供失物招领、图书管理、课程信息、学习小组等功能。

## 📋 功能特性

- 🔐 **用户认证系统** - 安全的登录注册功能
- 📚 **图书管理** - 图书借阅、归还、搜索
- 🎯 **课程管理** - 课程信息查看、选课功能
- 👥 **学习小组** - 创建和加入学习小组
- 🔍 **失物招领** - 发布和查找丢失物品
- 👨‍💼 **管理员后台** - 系统管理和数据维护

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Flask 2.0+
- SQLite 3

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://gitee.com/ospuer/kunqing.git
   cd kunqing-campus
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   python run.py
   ```

5. **访问应用**
   - 打开浏览器访问: http://127.0.0.1:5000
   - 使用测试账户登录：
     - **管理员账户**: 用户名: `admin` 密码: `123456` (管理员级别: 2)
     - **普通用户**: 用户名: `2021001` 密码: `password123`
     - **普通用户**: 用户名: `2021002` 密码: `password123`

## 📁 项目结构

```
kunqing-campus/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂
│   ├── simple_models.py   # 数据模型
│   ├── routes/            # 路由模块
│   │   ├── auth.py        # 认证路由
│   │   ├── simple_books.py      # 图书管理
│   │   ├── simple_courses.py    # 课程管理
│   │   ├── simple_lost_found.py # 失物招领
│   │   └── simple_study_groups.py # 学习小组
│   ├── templates/         # HTML模板
│   ├── static/           # 静态文件
│   └── utils/            # 工具函数
├── config.py             # 配置文件
├── run.py               # 启动文件
├── requirements.txt     # 依赖列表
├── kunqing.sqlite      # SQLite数据库
└── Git使用指南.md       # Git使用文档
```

## 🔧 开发指南

### 数据库初始化
```python
from app.simple_models import init_db, init_sample_data

# 初始化数据库表
init_db()

# 创建示例数据
init_sample_data()
```

### 管理员登录与权限说明
- 管理员登录入口：访问 `http://127.0.0.1:5000/admin/login`
- 设置页权限：`/admin/settings` 需要“超级管理员”权限（`admin_level=2` 或用户名为 `admin`）。
- 首次登录迁移：如果数据库中管理员密码是旧版 SHA256（如 `123456`），系统会在首次登录时自动迁移为 bcrypt 存储，无需手动操作。
- 检查数据库用户：运行 `python scripts/check_db.py` 可查看当前 `kunqing.sqlite` 中的用户与权限等级。

### 邮件 SMTP 配置与测试
系统支持在“管理员后台 → 系统设置”页面进行 SMTP 自检与邮件发送测试，并在页面内联展示结果（包含耗时与错误信息）。

- 环境配置（可放入系统环境变量或 `config.py`）：
  - `MAIL_SERVER`：SMTP服务器地址，例如 `smtp.qq.com`
  - `MAIL_PORT`：SMTP端口，例如 `587`
  - `MAIL_USE_TLS`：是否使用 TLS（推荐）
  - `MAIL_USE_SSL`：是否使用 SSL（通常与 TLS 互斥）
  - `MAIL_USERNAME`：SMTP登录用户名（通常为发件邮箱）
  - `MAIL_PASSWORD`：SMTP登录密码或授权码（QQ邮箱需使用授权码）
  - `MAIL_DEFAULT_SENDER`：默认发件人邮箱

- 使用方法：
  - 在“测试收件人”输入框中填写目标邮箱（必填）。
  - 点击“测试SMTP配置”或“测试邮件”按钮发起测试。
  - 结果面板会显示：`ok`、`server`、`port`、`use_tls`、`sender`、`recipient`、`duration_ms`、`error` 等字段。

- QQ 邮箱示例：
  - `MAIL_SERVER=smtp.qq.com`
  - `MAIL_PORT=587`
  - `MAIL_USE_TLS=True`
  - `MAIL_USERNAME=你的QQ邮箱`
  - `MAIL_PASSWORD=你的QQ邮箱授权码`
  - `MAIL_DEFAULT_SENDER=你的QQ邮箱`


### 添加新功能
1. 在 `app/routes/` 下创建新的路由文件
2. 在 `app/simple_models.py` 中添加相应的数据模型
3. 在 `app/templates/` 下创建HTML模板
4. 在 `app/__init__.py` 中注册新的蓝图

### 测试
```bash
# 运行登录功能测试
python test_login.py

# 运行Web API测试
python test_web_login.py
```

## 📚 Git 使用指南

本项目提供了完整的Git使用文档和自动化脚本：

### 📖 文档
- [Git使用指南.md](Git使用指南.md) - 详细的Git使用教程
- [Git快速命令.md](Git快速命令.md) - 常用命令速查表

### 🚀 自动化脚本

#### Windows用户
```powershell
# 使用默认提交信息
.\git-push.ps1

# 使用自定义提交信息
.\git-push.ps1 -message "feat: 添加新功能"

# 强制推送
.\git-push.ps1 -message "fix: 修复问题" -force
```

#### Linux/Mac用户
```bash
# 给脚本执行权限
chmod +x git-push.sh

# 使用默认提交信息
./git-push.sh

# 使用自定义提交信息
./git-push.sh "feat: 添加新功能"

# 推送到指定分支
./git-push.sh "update" develop
```

### 🔧 Git配置
```bash
# 设置用户信息
git config --global user.name "龚精奎"
git config --global user.email "2713878912@qq.com"

# 添加远程仓库
git remote add origin https://gitee.com/ospuer/kunqing.git
```

## 🌟 主要功能模块

### 用户认证 (`/auth`)
- 用户登录/注销
- 会话管理
- 权限控制

### 图书管理 (`/books`)
- 图书列表查看
- 图书搜索
- 借阅记录

### 课程管理 (`/courses`)
- 课程信息展示
- 课程搜索
- 选课功能

### 失物招领 (`/lost_found`)
- 发布丢失物品
- 发布拾到物品
- 物品搜索

### 学习小组 (`/study_groups`)
- 创建学习小组
- 加入小组
- 小组管理

### 管理员后台 (`/admin`)
- 用户管理
- 数据统计
- 系统设置

## 🔒 安全特性

- 密码哈希存储（bcrypt）
- 会话管理（Flask-Login）
- CSRF保护
- SQL注入防护
- XSS防护

## 🛠️ 技术栈

- **后端**: Flask, SQLite
- **前端**: HTML5, CSS3, JavaScript, Bootstrap
- **认证**: Flask-Login, bcrypt
- **数据库**: SQLite3
- **部署**: 支持多种部署方式

## 📝 开发规范

### 提交信息规范
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建过程

### 代码规范
- 遵循PEP 8规范
- 使用有意义的变量名
- 添加必要的注释
- 保持函数简洁

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目链接: [https://gitee.com/ospuer/kunqing](https://gitee.com/ospuer/kunqing)
- 问题反馈: 2713878912@qq.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**Happy Coding!** 🎉