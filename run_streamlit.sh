#!/bin/bash

# SmartDOX Streamlit App Launcher for Linux/macOS

echo "========================================="
echo "  SmartDOX - Tender Evaluation Platform"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[✓] Python found"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Check if requirements are installed
if ! pip3 list | grep -q "streamlit"; then
    echo "[!] Dependencies not installed"
    echo "Installing required packages..."
    pip3 install -r requirements_streamlit.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    echo "[✓] Dependencies installed"
else
    echo "[✓] Dependencies found"
fi

echo ""
echo "[!] Make sure:"
echo "    1. Backend API is running on http://localhost:8000"
echo "    2. Tesseract-OCR is installed"
echo "       - macOS: brew install tesseract"
echo "       - Linux: sudo apt-get install tesseract-ocr"
echo "    3. .env file is configured with API_BASE_URL"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[!] .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "[✓] .env file created. Please configure it before running the app."
    echo ""
fi

echo "Starting Streamlit app..."
echo ""

# Launch Streamlit
streamlit run app.py
