# Clean MindfulAI Project for GitHub Push

Write-Host "🧹 Cleaning MindfulAI for GitHub..." -ForegroundColor Green

# Remove Python cache
Write-Host "Removing Python cache..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force

# Remove user data
Write-Host "Removing user data..." -ForegroundColor Yellow
if (Test-Path "data/conversations") { Remove-Item "data/conversations" -Recurse -Force }
if (Test-Path "data/users") { Remove-Item "data/users" -Recurse -Force }
if (Test-Path "data/memory") { Remove-Item "data/memory" -Recurse -Force }
if (Test-Path "data/analytics") { Remove-Item "data/analytics" -Recurse -Force }

# Remove training models (too large)
Write-Host "Removing large models..." -ForegroundColor Yellow
if (Test-Path "training/naina_final_model") { Remove-Item "training/naina_final_model" -Recurse -Force }
if (Test-Path "training/naina_model") { Remove-Item "training/naina_model" -Recurse -Force }

# Remove IDE settings
Write-Host "Removing IDE files..." -ForegroundColor Yellow
if (Test-Path ".vscode") { Remove-Item ".vscode" -Recurse -Force }
if (Test-Path ".idea") { Remove-Item ".idea" -Recurse -Force }

# Remove virtual environment
Write-Host "Removing virtual environment..." -ForegroundColor Yellow
if (Test-Path "mindful_env") { Remove-Item "mindful_env" -Recurse -Force }
if (Test-Path "venv") { Remove-Item "venv" -Recurse -Force }

# Remove .env file
Write-Host "Removing .env file..." -ForegroundColor Yellow
if (Test-Path ".env") { Remove-Item ".env" -Force }

# Remove backup files
Write-Host "Removing backups..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include *.bak,*.backup -Recurse -Force | Remove-Item -Force

# Remove OS files
Write-Host "Removing OS files..." -ForegroundColor Yellow
Get-ChildItem -Path . -Include .DS_Store,Thumbs.db -Recurse -Force | Remove-Item -Force

Write-Host ""
Write-Host "✅ Project cleaned for GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. git init" -ForegroundColor White
Write-Host "2. git add ." -ForegroundColor White
Write-Host "3. git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "4. git push" -ForegroundColor White
