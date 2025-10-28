@echo off
echo ========================================
echo Sports Medicine - ONE CLICK LAUNCHER
echo ========================================
echo.
echo This will automatically:
echo  - Check prerequisites
echo  - Install dependencies (if needed)
echo  - Start the application
echo.
echo Please wait, this may take a few minutes on first run...
echo.
pause

REM ===========================
REM STEP 1: Check Prerequisites
REM ===========================
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is NOT installed!
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org/downloads/
    echo 2. Download Python 3.9 or newer
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart your computer after installing
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)
python --version
echo Python is installed!

echo.
echo [2/7] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Node.js is NOT installed!
    echo.
    echo Please install Node.js first:
    echo 1. Go to https://nodejs.org/
    echo 2. Download the LTS version
    echo 3. Install with default settings
    echo 4. Restart your computer after installing
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)
node --version
echo Node.js is installed!

REM ===========================
REM STEP 2: Setup Virtual Environment
REM ===========================
echo.
echo [3/7] Setting up Python virtual environment...
if exist "venv\" (
    echo Virtual environment already exists.
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created!
)

REM ===========================
REM STEP 3: Install Backend Dependencies
REM ===========================
echo.
echo [4/7] Checking backend dependencies...
call venv\Scripts\activate.bat

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo Backend dependencies not found. Installing...
    echo This will take 2-3 minutes...
    echo.

    echo Upgrading pip...
    python -m pip install --upgrade pip --quiet

    echo Installing backend packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install backend dependencies!
        echo Please check your internet connection and try again.
        echo If problem persists, run as Administrator.
        echo.
        pause
        exit /b 1
    )
    echo Backend dependencies installed successfully!
) else (
    echo Backend dependencies already installed.
)

REM ===========================
REM STEP 4: Install Frontend Dependencies
REM ===========================
echo.
echo [5/7] Checking frontend dependencies...
if exist "frontend\node_modules\vite\" (
    echo Frontend dependencies already installed.
) else (
    echo Frontend dependencies not found. Installing...
    echo This will take 3-5 minutes...
    echo.

    cd frontend
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install frontend dependencies!
        echo Please check your internet connection and try again.
        echo.
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo Frontend dependencies installed successfully!
)

REM ===========================
REM STEP 5: Start Backend Server
REM ===========================
echo.
echo [6/7] Starting Backend Server...
start "Sports Medicine - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python run_backend.py"
echo Backend server starting...

REM Wait for backend to initialize
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak > nul

REM ===========================
REM STEP 6: Start Frontend Server
REM ===========================
echo.
echo [7/7] Starting Frontend Server...
start "Sports Medicine - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo Frontend server starting...

REM Wait for frontend to initialize
echo Waiting for frontend to initialize (8 seconds)...
timeout /t 8 /nobreak > nul

REM ===========================
REM STEP 7: Open Browser
REM ===========================
echo.
echo ========================================
echo SUCCESS! Application Started!
echo ========================================
echo.
echo Two terminal windows have opened:
echo   1. Backend Server (http://127.0.0.1:8000)
echo   2. Frontend Server (http://127.0.0.1:3000)
echo.
echo IMPORTANT: Keep both windows open while using the app!
echo.
echo Opening browser now...
timeout /t 2 /nobreak > nul

start http://127.0.0.1:3000

echo.
echo ========================================
echo Application is running!
echo ========================================
echo.
echo Your browser should open automatically.
echo If not, manually go to: http://127.0.0.1:3000
echo.
echo To stop the application:
echo   - Close both terminal windows
echo   OR
echo   - Run STOP_APP.bat
echo.
echo Enjoy using the Sports Medicine System!
echo.
pause
