# Git项目初始化指南 🚀

本指南将帮助您将鲲擎校园系统项目上传到GitHub/GitLab等Git托管平台。

## 📋 前置准备

### 1. 安装Git
```bash
# Windows: 下载并安装 Git for Windows
# https://git-scm.com/download/win

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git

# Linux (CentOS/RHEL)
sudo yum install git

# macOS
brew install git
```

### 2. 配置Git用户信息
```bash
# 设置全局用户名和邮箱（必须）
git config --global user.name "你的用户名"
git config --global user.email "your.email@example.com"

# 验证配置
git config --global --list
```

### 3. 生成SSH密钥（推荐）
```bash
# 生成SSH密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 查看公钥内容
cat ~/.ssh/id_rsa.pub

# Windows用户使用：
type %USERPROFILE%\.ssh\id_rsa.pub
```

## 🌐 创建远程仓库

### GitHub
1. 登录 [GitHub](https://github.com)
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - Repository name: `kunqing-campus`
   - Description: `鲲擎校园综合服务平台`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"
5. 复制仓库URL：
   - HTTPS: `https://github.com/你的用户名/kunqing-campus.git`
   - SSH: `git@github.com:你的用户名/kunqing-campus.git`

### GitLab
1. 登录 [GitLab](https://gitlab.com)
2. 点击 "New project" → "Create blank project"
3. 填写项目信息：
   - Project name: `kunqing-campus`
   - Project description: `鲲擎校园综合服务平台`
   - Visibility Level: Public 或 Private
   - **不要**勾选 "Initialize repository with a README"
4. 点击 "Create project"
5. 复制仓库URL

### Gitee（码云）
1. 登录 [Gitee](https://gitee.com)
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - 仓库名称: `kunqing-campus`
   - 仓库介绍: `鲲擎校园综合服务平台`
   - 选择开源或私有
   - **不要**勾选 "使用Readme文件初始化这个仓库"
4. 点击 "创建"
5. 复制仓库URL

## 🚀 项目初始化和上传

### 方法一：使用自动化脚本（推荐）

#### Windows用户
```powershell
# 1. 初始化Git仓库
git init

# 2. 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/kunqing-campus.git

# 3. 使用自动化脚本上传
.\git-push.ps1 -message "feat: 初始化鲲擎校园系统项目"
```

#### Linux/Mac用户
```bash
# 1. 初始化Git仓库
git init

# 2. 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/kunqing-campus.git

# 3. 给脚本执行权限
chmod +x git-push.sh

# 4. 使用自动化脚本上传
./git-push.sh "feat: 初始化鲲擎校园系统项目"
```

### 方法二：手动执行Git命令

```bash
# 1. 初始化Git仓库
git init

# 2. 添加所有文件到暂存区
git add .

# 3. 创建初始提交
git commit -m "feat: 初始化鲲擎校园系统项目"

# 4. 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/kunqing-campus.git

# 5. 推送到远程仓库
git push -u origin main
```

## 🔧 常见问题解决

### 1. 推送失败：remote rejected
```bash
# 如果远程仓库有README等文件，需要先拉取
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### 2. 认证失败
```bash
# 使用SSH方式（推荐）
git remote set-url origin git@github.com:你的用户名/kunqing-campus.git

# 或者使用个人访问令牌（GitHub）
# 在GitHub设置中生成Personal Access Token，用作密码
```

### 3. 分支名称问题
```bash
# 如果默认分支是master，改为main
git branch -M main
git push -u origin main
```

### 4. 文件过大问题
```bash
# 如果有大文件，添加到.gitignore
echo "*.sqlite" >> .gitignore
echo "*.log" >> .gitignore
git add .gitignore
git commit -m "chore: 添加.gitignore文件"
```

## 📝 提交信息规范

使用语义化提交信息：

```bash
# 新功能
git commit -m "feat: 添加用户登录功能"

# 修复bug
git commit -m "fix: 修复登录验证问题"

# 文档更新
git commit -m "docs: 更新README文档"

# 代码重构
git commit -m "refactor: 重构用户模型"

# 性能优化
git commit -m "perf: 优化数据库查询性能"

# 测试相关
git commit -m "test: 添加登录功能测试"

# 构建相关
git commit -m "chore: 更新依赖包版本"
```

## 🔄 后续开发流程

### 日常开发
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 创建功能分支（可选）
git checkout -b feature/new-feature

# 3. 开发完成后提交
git add .
git commit -m "feat: 添加新功能"

# 4. 推送到远程
git push origin feature/new-feature

# 5. 合并到主分支
git checkout main
git merge feature/new-feature
git push origin main
```

### 使用自动化脚本
```bash
# Windows
.\git-push.ps1 -message "feat: 添加新功能"

# Linux/Mac
./git-push.sh "feat: 添加新功能"
```

## 🌟 最佳实践

### 1. 提交频率
- 小步快跑，频繁提交
- 每个提交只包含一个逻辑变更
- 提交前确保代码可以运行

### 2. 分支管理
- `main/master`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

### 3. 代码审查
- 使用Pull Request/Merge Request
- 代码审查后再合并
- 保持代码质量

### 4. 备份策略
- 定期推送到远程仓库
- 重要节点打标签
- 多个远程仓库备份

## 📞 获取帮助

如果遇到问题，可以：

1. 查看Git官方文档：https://git-scm.com/doc
2. 查看GitHub帮助：https://docs.github.com
3. 使用Git命令帮助：`git help <command>`
4. 在线Git教程：https://learngitbranching.js.org

---

**祝您使用愉快！** 🎉