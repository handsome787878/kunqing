# Git 使用指南 - 鲲擎校园系统

## 📋 目录
1. [Git 初始配置](#git-初始配置)
2. [创建本地仓库](#创建本地仓库)
3. [连接远程仓库](#连接远程仓库)
4. [基本操作流程](#基本操作流程)
5. [分支管理](#分支管理)
6. [常用命令速查](#常用命令速查)
7. [问题解决](#问题解决)

---

## 🔧 Git 初始配置

### 1. 设置用户信息
```bash
# 设置全局用户名（必须）
git config --global user.name "你的用户名"

# 设置全局邮箱（必须）
git config --global user.email "your.email@example.com"

# 查看当前配置
git config --list
```

### 2. 配置SSH密钥（推荐）
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 查看公钥内容（复制到GitHub/GitLab等平台）
cat ~/.ssh/id_rsa.pub

# 测试SSH连接
ssh -T git@github.com
```

---

## 📁 创建本地仓库

### 方法一：从现有项目初始化
```bash
# 进入项目目录
cd /path/to/kunqing-campus

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 创建首次提交
git commit -m "Initial commit: 鲲擎校园系统初始版本"
```

### 方法二：克隆远程仓库
```bash
# 克隆仓库
git clone https://github.com/username/kunqing-campus.git

# 或使用SSH（推荐）
git clone git@github.com:username/kunqing-campus.git
```

---

## 🌐 连接远程仓库

### 1. 添加远程仓库
```bash
# 添加GitHub远程仓库
git remote add origin https://github.com/你的用户名/kunqing-campus.git

# 或使用SSH（推荐）
git remote add origin git@github.com:你的用户名/kunqing-campus.git

# 查看远程仓库
git remote -v
```

### 2. 首次推送
```bash
# 推送到远程仓库的main分支
git push -u origin main

# 如果远程仓库是空的，可能需要先创建main分支
git branch -M main
git push -u origin main
```

---

## 🔄 基本操作流程

### 日常开发流程
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 查看文件状态
git status

# 3. 添加修改的文件
git add .                    # 添加所有文件
git add app/routes/auth.py   # 添加特定文件
git add app/                 # 添加整个目录

# 4. 提交更改
git commit -m "feat: 修复登录功能问题"

# 5. 推送到远程仓库
git push origin main
```

### 提交信息规范
```bash
# 功能添加
git commit -m "feat: 添加用户登录功能"

# 问题修复
git commit -m "fix: 修复密码验证逻辑错误"

# 文档更新
git commit -m "docs: 更新API文档"

# 样式调整
git commit -m "style: 调整登录页面样式"

# 重构代码
git commit -m "refactor: 重构用户模型代码"

# 性能优化
git commit -m "perf: 优化数据库查询性能"

# 测试相关
git commit -m "test: 添加登录功能测试用例"
```

---

## 🌿 分支管理

### 创建和切换分支
```bash
# 创建新分支
git branch feature/user-management

# 切换到分支
git checkout feature/user-management

# 创建并切换到新分支（推荐）
git checkout -b feature/user-management

# 查看所有分支
git branch -a
```

### 分支合并
```bash
# 切换到主分支
git checkout main

# 合并功能分支
git merge feature/user-management

# 删除已合并的分支
git branch -d feature/user-management

# 推送删除远程分支
git push origin --delete feature/user-management
```

---

## 📚 常用命令速查

### 查看信息
```bash
git status              # 查看工作区状态
git log                 # 查看提交历史
git log --oneline       # 简洁的提交历史
git diff                # 查看未暂存的更改
git diff --staged       # 查看已暂存的更改
git show HEAD           # 查看最近一次提交
```

### 撤销操作
```bash
git checkout -- file.py        # 撤销工作区的修改
git reset HEAD file.py         # 取消暂存
git reset --soft HEAD~1        # 撤销最近一次提交（保留更改）
git reset --hard HEAD~1        # 撤销最近一次提交（丢弃更改）
```

### 远程操作
```bash
git fetch origin               # 获取远程更新
git pull origin main           # 拉取并合并
git push origin main           # 推送到远程
git push --force origin main   # 强制推送（谨慎使用）
```

---

## 🔧 问题解决

### 1. 推送被拒绝
```bash
# 问题：remote rejected
# 解决：先拉取远程更改
git pull origin main
git push origin main
```

### 2. 合并冲突
```bash
# 查看冲突文件
git status

# 手动解决冲突后
git add .
git commit -m "resolve: 解决合并冲突"
```

### 3. 忘记添加.gitignore
```bash
# 创建.gitignore文件
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "kunqing.sqlite" >> .gitignore

# 移除已跟踪的文件
git rm -r --cached __pycache__
git rm --cached kunqing.sqlite

# 提交更改
git add .gitignore
git commit -m "chore: 添加.gitignore文件"
```

### 4. 修改最近一次提交
```bash
# 修改提交信息
git commit --amend -m "新的提交信息"

# 添加遗漏的文件到最近一次提交
git add forgotten_file.py
git commit --amend --no-edit
```

---

## 📝 项目特定配置

### .gitignore 文件内容
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# Flask
instance/
.webassets-cache

# Database
*.sqlite
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local
.env.production

# Node modules (if using frontend build tools)
node_modules/
```

### 常用Git别名配置
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

---

## 🚀 快速开始示例

```bash
# 1. 配置Git（首次使用）
git config --global user.name "张三"
git config --global user.email "zhangsan@example.com"

# 2. 初始化项目
cd E:\APP\kunqing\kunqing-campus
git init
git add .
git commit -m "Initial commit: 鲲擎校园系统"

# 3. 连接GitHub仓库
git remote add origin https://github.com/zhangsan/kunqing-campus.git
git branch -M main
git push -u origin main

# 4. 日常开发
git add .
git commit -m "feat: 完善登录功能"
git push origin main
```

---

## 📞 获取帮助

```bash
git help                    # Git帮助
git help <command>          # 特定命令帮助
git <command> --help        # 命令帮助
```

---

**注意事项：**
- 🔒 不要提交敏感信息（密码、密钥等）
- 📝 提交信息要清晰明确
- 🌿 使用分支进行功能开发
- 🔄 定期同步远程仓库
- 📋 遵循团队的Git工作流程

**祝你使用鲲擎校园系统愉快！** 🎉