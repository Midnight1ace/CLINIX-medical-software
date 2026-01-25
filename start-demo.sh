#!/bin/bash

echo "============================================================"
echo " AI-Patient-Record-Intelligence Demo Launcher"
echo "============================================================"
echo ""

DEMO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/4] Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.9+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "[2/4] Setting up backend..."
echo "Creating virtual environment..."

cd "$DEMO_DIR/backend"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "Installing backend dependencies..."
source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo "[3/4] Setting up frontend..."
cd "$DEMO_DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies (this may take a minute)..."
    npm install --silent
else
    echo "Frontend dependencies already installed."
fi

echo ""
echo "[4/4] Starting servers..."
echo ""
echo "============================================================"
echo " Backend:  http://localhost:8000"
echo " Frontend: http://localhost:5173"
echo "============================================================"
echo ""
echo "Demo Credentials:"
echo "  Doctor:     dr_johnson / demo123"
echo "  Pharmacist: pharm_smith / demo123"
echo ""
echo "Demo Patients:"
echo "  PAT_987654 - John Smith (64M)"
echo "  PAT_654321 - Mary Johnson (69F)"
echo ""
echo "============================================================"
echo ""

trap 'echo ""; echo "Shutting down servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo "Servers stopped. Demo ended."; exit' INT TERM

echo "Starting backend server..."
cd "$DEMO_DIR/backend"
source venv/bin/activate
python main.py &
BACKEND_PID=$!

sleep 3

echo "Starting frontend server..."
cd "$DEMO_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Servers started!"
echo ""
echo "Opening browser in 5 seconds..."
sleep 5

if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5173
elif command -v open &> /dev/null; then
    open http://localhost:5173
fi

echo ""
echo "Press Ctrl+C to stop all servers and exit."
echo ""

wait
