# Axiom Canvas - Quick Start Script for Windows
# This script helps you set up and run the application locally

Write-Host "🚀 Axiom Canvas - Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 is not installed. Please install Python 3.11 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "📥 Activating virtual environment..." -ForegroundColor Yellow

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt | Out-Null

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check for .env file
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "📝 Please edit .env and add your GEMINI_API_KEY" -ForegroundColor Cyan
    Write-Host "   Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    # Open .env in default text editor
    notepad .env
    
    Read-Host "Press Enter after you've added your API key to .env"
}

# Load environment variables from .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        Set-Item -Path "env:$name" -Value $value
    }
}

# Check if API key is set
if (-Not $env:GEMINI_API_KEY -or $env:GEMINI_API_KEY -eq "your_gemini_api_key_here") {
    Write-Host "❌ GEMINI_API_KEY not set in .env file" -ForegroundColor Red
    Write-Host "   Please edit .env and add your API key" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Environment variables loaded" -ForegroundColor Green
Write-Host ""

# Run the application
Write-Host "🎉 Starting Axiom Canvas..." -ForegroundColor Green
Write-Host "   Access the app at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

Set-Location api
python index.py
