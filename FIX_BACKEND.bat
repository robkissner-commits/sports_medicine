@echo off
echo ========================================
echo FIX: Install Backend Dependencies
echo ========================================
echo.
echo This will install all required Python packages.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python is installed:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing backend dependencies...
echo This may take 2-3 minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Try these solutions:
    echo 1. Make sure you have internet connection
    echo 2. Run this script as Administrator
    echo 3. Check if antivirus is blocking pip
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Backend dependencies installed!
echo ========================================
echo.
echo You can now run START_APP.bat
echo.
pause
