@echo off
REM SmartDOX Streamlit App Launcher for Windows

echo =========================================
echo   SmartDOX - Tender Evaluation Platform
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if requirements are installed
pip list | findstr /i "streamlit" >nul
if errorlevel 1 (
    echo [!] Dependencies not installed
    echo Installing required packages...
    pip install -r requirements_streamlit.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
    echo [✓] Dependencies installed
) else (
    echo [✓] Dependencies found
)

echo.
echo [!] Make sure:
echo     1. Backend API is running on http://localhost:8000
echo     2. Tesseract-OCR is installed (https://github.com/UB-Mannheim/tesseract/wiki)
echo     3. .env file is configured with API_BASE_URL
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [!] .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo [✓] .env file created. Please configure it before running the app.
    echo.
)

echo Starting Streamlit app...
echo.

REM Launch Streamlit
streamlit run app.py

pause
