# Kunqing Campus

一个基于 Flask 的校园应用项目结构。

## 结构

```
kunqing-campus/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── lost_found.py
│   │   ├── books.py
│   │   ├── courses.py
│   │   └── study_groups.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── lost_found/
│   │   ├── books/
│   │   ├── courses/
│   │   └── study_groups/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py
│       └── helpers.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行开发服务器：
   ```bash
   python run.py
   ```

访问 `http://127.0.0.1:5000/`，各模块示例首页：

- 认证：`/auth/`
- 失物招领：`/lost-found/`
- 图书：`/books/`
- 课程：`/courses/`
- 学习小组：`/study-groups/`
- 示例用户：用户名 2021001 ，密码 password123
- 示例用户：用户名 2021002 ，密码 password123