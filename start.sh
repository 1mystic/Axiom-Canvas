#!/bin/bash

# Axiom Canvas - Quick Start Script
# This script helps you set up and run the application locally

echo "🚀 Axiom Canvas - Quick Start"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "📥 Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env and add your GEMINI_API_KEY"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your_gemini_api_key_here" ]; then
    echo "❌ GEMINI_API_KEY not set in .env file"
    echo "   Please edit .env and add your API key"
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Run the application
echo "🎉 Starting Axiom Canvas..."
echo "   Access the app at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd api
python index.py
