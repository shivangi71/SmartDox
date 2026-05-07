@echo off
REM Quick Tesseract-OCR Installation Script for Windows

echo =========================================
echo   Tesseract-OCR Installer for SmartDOX
echo =========================================
echo.

REM Check if Tesseract is already installed
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo [✓] Tesseract-OCR is already installed at:
    echo     C:\Program Files\Tesseract-OCR
    echo.
    echo You can now use the app to process image files.
    pause
    exit /b 0
)

if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
    echo [✓] Tesseract-OCR is already installed at:
    echo     C:\Program Files (x86)\Tesseract-OCR
    echo.
    echo You can now use the app to process image files.
    pause
    exit /b 0
)

echo [!] Tesseract-OCR not found.
echo.
echo To install Tesseract-OCR manually:
echo.
echo 1. Download the installer from:
echo    https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo 2. Look for the latest release (e.g., tesseract-ocr-w64-v5.x.exe)
echo.
echo 3. Run the installer and choose installation directory:
echo    Default: C:\Program Files\Tesseract-OCR
echo.
echo 4. During installation, select "Additional language data" if needed
echo.
echo 5. After installation, restart the Streamlit app
echo.
echo Alternative (using Chocolatey, if installed):
echo   choco install tesseract
echo.
pause
