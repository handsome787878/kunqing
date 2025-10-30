# Git 自动上传脚本 - 鲲擎校园系统
# 使用方法: .\git-push.ps1 -message "你的提交信息"

param(
    [string]$message = "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    [string]$branch = "main",
    [switch]$force = $false
)

# 设置控制台编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "     鲲擎校园系统 - Git 自动上传工具" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在Git仓库中
if (-not (Test-Path ".git")) {
    Write-Host "❌ 错误: 当前目录不是Git仓库！" -ForegroundColor Red
    Write-Host "请在项目根目录运行此脚本。" -ForegroundColor Yellow
    exit 1
}

try {
    # 显示当前状态
    Write-Host "📋 检查当前状态..." -ForegroundColor Green
    git status --porcelain
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git status 命令失败"
    }

    # 检查是否有更改
    $changes = git status --porcelain
    if (-not $changes) {
        Write-Host "✅ 没有需要提交的更改。" -ForegroundColor Yellow
        exit 0
    }

    Write-Host ""
    Write-Host "📁 添加所有更改到暂存区..." -ForegroundColor Green
    git add .
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git add 命令失败"
    }

    Write-Host ""
    Write-Host "📝 提交更改..." -ForegroundColor Green
    Write-Host "提交信息: $message" -ForegroundColor Cyan
    git commit -m $message
    
    if ($LASTEXITCODE -ne 0) {
        throw "Git commit 命令失败"
    }

    Write-Host ""
    Write-Host "🔄 推送到远程仓库 ($branch 分支)..." -ForegroundColor Green
    
    if ($force) {
        Write-Host "⚠️  使用强制推送..." -ForegroundColor Yellow
        git push --force origin $branch
    } else {
        git push origin $branch
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 推送失败，尝试先拉取远程更改..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "🔽 拉取远程更改..." -ForegroundColor Green
        git pull origin $branch
        
        if ($LASTEXITCODE -ne 0) {
            throw "Git pull 命令失败，可能存在冲突"
        }
        
        Write-Host "🔄 重新推送..." -ForegroundColor Green
        git push origin $branch
        
        if ($LASTEXITCODE -ne 0) {
            throw "Git push 命令失败"
        }
    }

    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host "🎉 成功上传到远程仓库！" -ForegroundColor Green
    Write-Host "===========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 最近的提交:" -ForegroundColor Cyan
    git log --oneline -5
    
} catch {
    Write-Host ""
    Write-Host "===========================================" -ForegroundColor Red
    Write-Host "❌ 操作失败: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "===========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 可能的解决方案:" -ForegroundColor Yellow
    Write-Host "1. 检查网络连接" -ForegroundColor White
    Write-Host "2. 确认远程仓库地址正确" -ForegroundColor White
    Write-Host "3. 检查是否有合并冲突需要解决" -ForegroundColor White
    Write-Host "4. 确认有推送权限" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 手动解决步骤:" -ForegroundColor Yellow
    Write-Host "git status" -ForegroundColor Gray
    Write-Host "git pull origin $branch" -ForegroundColor Gray
    Write-Host "# 解决冲突后:" -ForegroundColor Gray
    Write-Host "git add ." -ForegroundColor Gray
    Write-Host "git commit -m `"resolve conflicts`"" -ForegroundColor Gray
    Write-Host "git push origin $branch" -ForegroundColor Gray
    
    exit 1
}

Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")