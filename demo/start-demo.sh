#!/bin/bash

# AI-Patient-Record-Intelligence DEMO - Quick Start Script
# Run: bash start-demo.sh

echo "🏥 AI-Patient-Record-Intelligence DEMO"
echo "Doctor-first clinical clarity"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

echo ""
echo "Starting AI-Patient-Record-Intelligence DEMO..."
echo ""

# Start Backend
echo "📦 Starting Backend (FastAPI)..."
cd "$(dirname "$0")/backend"
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt

echo "✅ Backend ready on http://localhost:8000"
python3 main.py &
BACKEND_PID=$!

# Wait for backend
sleep 2

# Start Frontend
echo "📦 Starting Frontend (React)..."
cd "$(dirname "$0")/frontend"
npm install -q
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Demo started!"
echo ""
echo "📍 Frontend:   http://localhost:5173"
echo "📍 Backend:    http://localhost:8000"
echo ""
echo "🔐 Demo Credentials:"
echo "   Doctor:     dr_johnson / demo123"
echo "   Doctor:     dr_hassan / demo123"
echo "   Pharmacist: pharm_smith / demo123"
echo ""
echo "🧪 Patient ID to search: PAT_987654"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
