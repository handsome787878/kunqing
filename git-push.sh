#!/bin/bash
# Git 自动上传脚本 - 鲲擎校园系统
# 使用方法: ./git-push.sh "你的提交信息"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# 默认参数
MESSAGE=${1:-"Update: $(date '+%Y-%m-%d %H:%M:%S')"}
BRANCH=${2:-"main"}
FORCE=${3:-false}

# 显示标题
echo -e "${CYAN}==========================================="
echo -e "     鲲擎校园系统 - Git 自动上传工具"
echo -e "===========================================${NC}"
echo ""

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ 错误: 当前目录不是Git仓库！${NC}"
    echo -e "${YELLOW}请在项目根目录运行此脚本。${NC}"
    exit 1
fi

# 错误处理函数
handle_error() {
    echo ""
    echo -e "${RED}==========================================="
    echo -e "❌ 操作失败: $1"
    echo -e "===========================================${NC}"
    echo ""
    echo -e "${YELLOW}💡 可能的解决方案:${NC}"
    echo -e "${WHITE}1. 检查网络连接${NC}"
    echo -e "${WHITE}2. 确认远程仓库地址正确${NC}"
    echo -e "${WHITE}3. 检查是否有合并冲突需要解决${NC}"
    echo -e "${WHITE}4. 确认有推送权限${NC}"
    echo ""
    echo -e "${YELLOW}🔧 手动解决步骤:${NC}"
    echo -e "${GRAY}git status${NC}"
    echo -e "${GRAY}git pull origin $BRANCH${NC}"
    echo -e "${GRAY}# 解决冲突后:${NC}"
    echo -e "${GRAY}git add .${NC}"
    echo -e "${GRAY}git commit -m \"resolve conflicts\"${NC}"
    echo -e "${GRAY}git push origin $BRANCH${NC}"
    exit 1
}

# 主要操作
main() {
    # 显示当前状态
    echo -e "${GREEN}📋 检查当前状态...${NC}"
    if ! git status --porcelain > /dev/null 2>&1; then
        handle_error "Git status 命令失败"
    fi

    # 检查是否有更改
    changes=$(git status --porcelain)
    if [ -z "$changes" ]; then
        echo -e "${YELLOW}✅ 没有需要提交的更改。${NC}"
        exit 0
    fi

    echo ""
    echo -e "${GREEN}📁 添加所有更改到暂存区...${NC}"
    if ! git add .; then
        handle_error "Git add 命令失败"
    fi

    echo ""
    echo -e "${GREEN}📝 提交更改...${NC}"
    echo -e "${CYAN}提交信息: $MESSAGE${NC}"
    if ! git commit -m "$MESSAGE"; then
        handle_error "Git commit 命令失败"
    fi

    echo ""
    echo -e "${GREEN}🔄 推送到远程仓库 ($BRANCH 分支)...${NC}"
    
    if [ "$FORCE" = "true" ]; then
        echo -e "${YELLOW}⚠️  使用强制推送...${NC}"
        if ! git push --force origin "$BRANCH"; then
            handle_error "强制推送失败"
        fi
    else
        if ! git push origin "$BRANCH"; then
            echo -e "${YELLOW}❌ 推送失败，尝试先拉取远程更改...${NC}"
            echo ""
            echo -e "${GREEN}🔽 拉取远程更改...${NC}"
            if ! git pull origin "$BRANCH"; then
                handle_error "Git pull 命令失败，可能存在冲突"
            fi
            
            echo -e "${GREEN}🔄 重新推送...${NC}"
            if ! git push origin "$BRANCH"; then
                handle_error "Git push 命令失败"
            fi
        fi
    fi

    echo ""
    echo -e "${GREEN}==========================================="
    echo -e "🎉 成功上传到远程仓库！"
    echo -e "===========================================${NC}"
    echo ""
    echo -e "${CYAN}📊 最近的提交:${NC}"
    git log --oneline -5
}

# 显示使用帮助
show_help() {
    echo -e "${CYAN}使用方法:${NC}"
    echo -e "${WHITE}  ./git-push.sh [提交信息] [分支名] [是否强制推送]${NC}"
    echo ""
    echo -e "${CYAN}示例:${NC}"
    echo -e "${WHITE}  ./git-push.sh                           # 使用默认提交信息${NC}"
    echo -e "${WHITE}  ./git-push.sh \"feat: 添加新功能\"        # 自定义提交信息${NC}"
    echo -e "${WHITE}  ./git-push.sh \"fix: 修复bug\" develop   # 推送到develop分支${NC}"
    echo -e "${WHITE}  ./git-push.sh \"update\" main true      # 强制推送${NC}"
    echo ""
    echo -e "${CYAN}参数说明:${NC}"
    echo -e "${WHITE}  提交信息: 描述本次提交的内容（可选）${NC}"
    echo -e "${WHITE}  分支名:   目标分支，默认为main（可选）${NC}"
    echo -e "${WHITE}  强制推送: true/false，默认为false（可选）${NC}"
}

# 检查参数
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

# 执行主要操作
main

echo ""
echo -e "${GRAY}按Enter键退出...${NC}"
read -r