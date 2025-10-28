@echo off
echo ========================================
echo FIX: Install Frontend Dependencies
echo ========================================
echo.
echo This will install all required Node.js packages.
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo.
    echo Please install Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed!
    echo Please reinstall Node.js from https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo Node.js is installed:
node --version
echo npm version:
npm --version
echo.

REM Go to frontend directory
if not exist "frontend\" (
    echo ERROR: frontend directory not found!
    echo Make sure you're running this from the sports_medicine folder.
    pause
    exit /b 1
)

cd frontend

REM Install dependencies
echo Installing frontend dependencies...
echo This may take 3-5 minutes...
echo.
call npm install
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install frontend dependencies
    echo.
    echo Try these solutions:
    echo 1. Make sure you have internet connection
    echo 2. Delete the node_modules folder and try again
    echo 3. Run this script as Administrator
    echo.
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo ========================================
echo SUCCESS! Frontend dependencies installed!
echo ========================================
echo.
echo You can now run START_APP.bat
echo.
pause
