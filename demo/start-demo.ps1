Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host " AI-Patient-Record-Intelligence Demo Launcher" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

$DEMO_DIR = $PSScriptRoot

Write-Host "[1/4] Checking prerequisites..." -ForegroundColor Yellow

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found. Please install Python 3.9-3.13" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Gray

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Host "ERROR: Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

$nodeVersion = & node --version 2>&1
Write-Host "Found: Node.js $nodeVersion" -ForegroundColor Gray

$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    Write-Host "ERROR: npm not found. Please install Node.js (includes npm)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/4] Setting up backend..." -ForegroundColor Yellow
Write-Host "Creating virtual environment..." -ForegroundColor Gray

Set-Location "$DEMO_DIR\backend"

if (!(Test-Path "venv")) {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Installing backend dependencies (this may take a minute)..." -ForegroundColor Gray
& "venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
& "venv\Scripts\python.exe" -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to install backend dependencies" -ForegroundColor Red
    Write-Host "If you're using Python 3.14, please use Python 3.9-3.13 instead." -ForegroundColor Yellow
    Write-Host "Python 3.14 is too new for current pydantic versions." -ForegroundColor Yellow
    exit 1
}

Write-Host "Backend dependencies installed successfully." -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] Setting up frontend..." -ForegroundColor Yellow
Set-Location "$DEMO_DIR\frontend"

if (!(Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies (this may take a minute)..." -ForegroundColor Gray
    & npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install frontend dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Frontend dependencies already installed." -ForegroundColor Gray
}

Write-Host "Frontend dependencies installed successfully." -ForegroundColor Green

Write-Host ""
Write-Host "[4/4] Starting servers..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host " Backend:  http://localhost:8000" -ForegroundColor Green
Write-Host " Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "Demo Credentials:" -ForegroundColor Yellow
Write-Host "  Doctor:     dr_johnson / demo123" -ForegroundColor White
Write-Host "  Pharmacist: pharm_smith / demo123" -ForegroundColor White
Write-Host ""
Write-Host "Demo Patients:" -ForegroundColor Yellow
Write-Host "  PAT_987654 - John Smith (64M)" -ForegroundColor White
Write-Host "  PAT_654321 - Mary Johnson (69F)" -ForegroundColor White
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting backend server..." -ForegroundColor Gray

try {
    $backend = Start-Process -FilePath "$DEMO_DIR\backend\venv\Scripts\python.exe" `
        -ArgumentList "$DEMO_DIR\backend\main.py" `
        -WorkingDirectory "$DEMO_DIR\backend" `
        -PassThru `
        -ErrorAction Stop
} catch {
    Write-Host "ERROR: Failed to start backend server" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

Start-Sleep -Seconds 3

Write-Host "Starting frontend server..." -ForegroundColor Gray

try {
    $npmPath = (Get-Command npm).Source
    $frontend = Start-Process -FilePath $npmPath `
        -ArgumentList "run", "dev" `
        -WorkingDirectory "$DEMO_DIR\frontend" `
        -PassThru `
        -ErrorAction Stop
} catch {
    Write-Host "ERROR: Failed to start frontend server" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($backend -and -not $backend.HasExited) {
        Stop-Process -Id $backend.Id -Force
    }
    exit 1
}

Write-Host ""
Write-Host "Servers started!" -ForegroundColor Green
Write-Host ""
Write-Host "Opening browser in 5 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Press Ctrl+C to stop all servers and exit." -ForegroundColor Cyan
Write-Host ""

try {
    while ($true) {
        if ($backend.HasExited) {
            Write-Host "Backend server has stopped unexpectedly." -ForegroundColor Red
            break
        }
        if ($frontend.HasExited) {
            Write-Host "Frontend server has stopped unexpectedly." -ForegroundColor Red
            break
        }
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host ""
    Write-Host "Shutting down servers..." -ForegroundColor Yellow
    
    if ($backend -and -not $backend.HasExited) {
        Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    }
    
    if ($frontend -and -not $frontend.HasExited) {
        Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "Servers stopped. Demo ended." -ForegroundColor Green
}
