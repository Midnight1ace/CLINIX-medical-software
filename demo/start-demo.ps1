# AI-Patient-Record-Intelligence DEMO - Quick Start Script
# Run this to start both backend and frontend

Write-Host "🏥 AI-Patient-Record-Intelligence DEMO" -ForegroundColor Cyan
Write-Host "Doctor-first clinical clarity" -ForegroundColor Gray
Write-Host ""

# Bypass execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Check if Python is installed
$pythonCheck = python --version 2>$null
if (-not $pythonCheck) {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python found: $pythonCheck" -ForegroundColor Green

# Check if Node is installed
$nodeCheck = node --version 2>$null
if (-not $nodeCheck) {
    Write-Host "❌ Node.js is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Node.js found: $nodeCheck" -ForegroundColor Green

Write-Host ""
Write-Host "Starting AI-Patient-Record-Intelligence DEMO..." -ForegroundColor Cyan
Write-Host ""

# Start Backend in new window
Write-Host "📦 Starting Backend (FastAPI)..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
$backendScript = @"
`$Host.UI.RawUI.WindowTitle = 'APRI Demo - Backend'
cd "$backendPath"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -q -r requirements.txt
Write-Host "✅ Backend ready on http://localhost:8000" -ForegroundColor Green
python main.py
"@

Start-Process powershell -ArgumentList "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", $backendScript

# Wait for backend to start
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Start Frontend in new window
Write-Host "📦 Starting Frontend (React)..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
$frontendScript = @"
`$Host.UI.RawUI.WindowTitle = 'APRI Demo - Frontend'
cd "$frontendPath"
npm install -q
npm run dev
"@

Start-Process powershell -ArgumentList "-ExecutionPolicy", "Bypass", "-NoExit", "-Command", $frontendScript

Write-Host ""
Write-Host "✅ Demo started!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend:   http://localhost:5173" -ForegroundColor Cyan
Write-Host "📍 Backend:    http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔐 Demo Credentials:" -ForegroundColor Yellow
Write-Host "   Doctor:   dr_johnson / demo123" -ForegroundColor Gray
Write-Host "   Doctor:   dr_hassan / demo123" -ForegroundColor Gray
Write-Host "   Pharmacist: pharm_smith / demo123" -ForegroundColor Gray
Write-Host ""
Write-Host "🧪 Patient ID to search: PAT_987654" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Gray
