#!/bin/bash

# Setup script for Resume-Job Matcher

set -e

echo "=========================================="
echo "Resume-Job Matcher Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi
echo "✓ Python version: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo "✓ NLTK data downloaded"

# Install frontend dependencies
echo ""
echo "Installing frontend dependencies..."
cd frontend
if command -v npm &> /dev/null; then
    npm install
    echo "✓ Frontend dependencies installed"
else
    echo "⚠ npm not found. Please install Node.js to build the frontend."
    echo "  You can still run the backend in API-only mode."
fi
cd ..

# Create data directory
echo ""
echo "Creating data directory..."
mkdir -p data
echo "✓ Data directory created"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (edit it if needed)"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "  Development mode (with hot-reload):"
echo "    1. Backend:  python backend/app.py"
echo "    2. Frontend: cd frontend && npm run dev"
echo ""
echo "  Production mode (with Docker):"
echo "    docker-compose up --build"
echo ""
echo "Then open http://localhost:5000 in your browser"
echo ""

