# Git 快速命令参考卡

## 🚀 一键上传脚本

### Windows PowerShell 脚本
```powershell
# 保存为 git-push.ps1
param(
    [string]$message = "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

Write-Host "开始Git操作..." -ForegroundColor Green
git add .
git status
git commit -m $message
git push origin main
Write-Host "上传完成！" -ForegroundColor Green
```

使用方法：
```powershell
# 使用默认提交信息
.\git-push.ps1

# 使用自定义提交信息
.\git-push.ps1 -message "feat: 添加新功能"
```

### Linux/Mac Bash 脚本
```bash
#!/bin/bash
# 保存为 git-push.sh

MESSAGE=${1:-"Update: $(date '+%Y-%m-%d %H:%M')"}

echo "开始Git操作..."
git add .
git status
git commit -m "$MESSAGE"
git push origin main
echo "上传完成！"
```

使用方法：
```bash
# 给脚本执行权限
chmod +x git-push.sh

# 使用默认提交信息
./git-push.sh

# 使用自定义提交信息
./git-push.sh "feat: 添加新功能"
```

---

## ⚡ 常用命令组合

### 初始化并上传项目
```bash
git init
git add .
git commit -m "Initial commit: 鲲擎校园系统"
git branch -M main
git remote add origin https://github.com/你的用户名/kunqing-campus.git
git push -u origin main
```

### 日常更新流程
```bash
git pull origin main    # 拉取最新代码
git add .              # 添加所有更改
git commit -m "描述"    # 提交更改
git push origin main   # 推送到远程
```

### 快速修复流程
```bash
git stash              # 暂存当前工作
git pull origin main   # 拉取最新代码
git stash pop          # 恢复暂存的工作
# 解决冲突（如果有）
git add .
git commit -m "fix: 修复问题"
git push origin main
```

---

## 🔧 实用别名配置

```bash
# 设置常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.ps push
git config --global alias.pl pull
git config --global alias.mg merge
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.amend 'commit --amend --no-edit'
```

使用别名：
```bash
git st          # 等同于 git status
git ci -m "msg" # 等同于 git commit -m "msg"
git lg          # 美化的日志显示
```

---

## 📋 提交信息模板

### 标准格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型说明
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```bash
git commit -m "feat(auth): 添加用户登录功能

- 实现用户名密码验证
- 添加会话管理
- 集成Flask-Login

Closes #123"
```

---

## 🌿 分支管理速查

```bash
# 分支操作
git branch                    # 查看本地分支
git branch -r                 # 查看远程分支
git branch -a                 # 查看所有分支
git branch feature-name       # 创建分支
git checkout feature-name     # 切换分支
git checkout -b feature-name  # 创建并切换分支
git branch -d feature-name    # 删除本地分支
git push origin --delete feature-name  # 删除远程分支

# 合并操作
git checkout main             # 切换到主分支
git merge feature-name        # 合并分支
git merge --no-ff feature-name # 非快进合并
```

---

## 🔄 同步操作

```bash
# 同步远程仓库
git fetch origin              # 获取远程更新
git pull origin main          # 拉取并合并
git push origin main          # 推送到远程

# 强制操作（谨慎使用）
git push --force origin main  # 强制推送
git reset --hard origin/main  # 强制同步远程
```

---

## 🚨 紧急情况处理

### 撤销最近提交
```bash
git reset --soft HEAD~1       # 撤销提交，保留更改
git reset --hard HEAD~1       # 撤销提交，丢弃更改
```

### 修改最近提交
```bash
git add forgotten-file.py     # 添加遗漏文件
git commit --amend --no-edit  # 修改最近提交
git commit --amend -m "新消息" # 修改提交信息
```

### 解决合并冲突
```bash
git status                    # 查看冲突文件
# 手动编辑冲突文件
git add .                     # 标记冲突已解决
git commit -m "resolve conflicts"  # 提交解决方案
```

---

## 📊 查看历史

```bash
git log                       # 详细日志
git log --oneline            # 简洁日志
git log --graph              # 图形化日志
git log --author="张三"       # 特定作者的提交
git log --since="2024-01-01" # 特定时间后的提交
git log --grep="登录"         # 搜索提交信息
git show HEAD                # 查看最近提交详情
git diff HEAD~1              # 与上一次提交比较
```

---

## 🔍 搜索和查找

```bash
git grep "function_name"      # 在代码中搜索
git log -S "function_name"    # 搜索添加/删除特定内容的提交
git blame filename           # 查看文件每行的修改者
git bisect start             # 二分查找问题提交
```

---

## 💡 实用技巧

### 1. 临时保存工作
```bash
git stash                     # 暂存当前工作
git stash pop                 # 恢复暂存的工作
git stash list                # 查看暂存列表
git stash drop                # 删除暂存
```

### 2. 选择性添加
```bash
git add -p                    # 交互式添加
git add -i                    # 交互式界面
```

### 3. 查看差异
```bash
git diff                      # 工作区与暂存区差异
git diff --staged             # 暂存区与仓库差异
git diff HEAD~1               # 与上次提交差异
```

---

## 📱 GitHub/GitLab 特定操作

### 创建Pull Request/Merge Request
```bash
git checkout -b feature/new-feature
# 开发功能
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature
# 在网页上创建PR/MR
```

### 同步Fork仓库
```bash
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

**记住：** 
- 🔄 经常提交，小步快跑
- 📝 写清楚的提交信息
- 🌿 使用分支开发功能
- 🔒 不要提交敏感信息
- 📋 遵循团队规范