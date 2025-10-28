@echo off
echo ========================================
echo First-Time Setup
echo Sports Medicine - Injury Prevention System
echo ========================================
echo.
echo This script will:
echo 1. Create Python virtual environment
echo 2. Install Python dependencies
echo 3. Install Node.js dependencies
echo.
echo This only needs to be run once!
echo.
pause

echo.
echo [1/3] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in your PATH
    pause
    exit /b 1
)
echo Virtual environment created!

echo.
echo [2/3] Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo Python dependencies installed!

echo.
echo [3/3] Installing Node.js dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    echo Make sure Node.js is installed
    cd ..
    pause
    exit /b 1
)
cd ..
echo Node.js dependencies installed!

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now run START_APP.bat to launch the application.
echo.
pause
