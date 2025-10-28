@echo off
echo ========================================
echo Sports Medicine - Injury Prevention System
echo ========================================
echo.
echo Starting application...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment and install dependencies if needed
if not exist "venv\Lib\site-packages\fastapi" (
    echo Installing backend dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo.
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo.
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
echo Backend will open at:  http://localhost:8000
echo Frontend will open at: http://localhost:3000
echo.
echo Two terminal windows will open:
echo   1. Backend Server (keep this open)
echo   2. Frontend Server (keep this open)
echo.
echo Press any key to open the application in your browser...
pause > nul

start http://localhost:3000

echo.
echo Application is running!
echo Close both terminal windows to stop the application.
echo.
