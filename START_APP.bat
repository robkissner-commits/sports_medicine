@echo off
echo ========================================
echo Sports Medicine - Injury Prevention System
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please download and install Python from: https://python.org
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo.
    echo Please download and install Node.js from: https://nodejs.org
    echo.
    pause
    exit /b 1
)

echo Starting application...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo.
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run one of these first:
    echo   1. SETUP.bat (full setup)
    echo   2. FIX_BACKEND.bat (just backend)
    echo.
    pause
    exit /b 1
)

REM Check if backend dependencies are installed by testing for uvicorn
call venv\Scripts\activate.bat
python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Backend dependencies not installed!
    echo.
    echo Please run FIX_BACKEND.bat to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules\vite" (
    echo.
    echo ERROR: Frontend dependencies not installed!
    echo.
    echo Please run FIX_FRONTEND.bat to install dependencies.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Backend Server...
echo ========================================
start "Sports Medicine - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python run_backend.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo Starting Frontend Server...
echo ========================================
start "Sports Medicine - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo Application is starting!
echo ========================================
echo.
echo Backend will open at:  http://127.0.0.1:8000
echo Frontend will open at: http://127.0.0.1:3000
echo.
echo Two terminal windows will open:
echo   1. Backend Server (keep this open)
echo   2. Frontend Server (keep this open)
echo.
echo Press any key to open the application in your browser...
pause > nul

start http://127.0.0.1:3000

echo.
echo Application is running!
echo Close both terminal windows to stop the application.
echo.
