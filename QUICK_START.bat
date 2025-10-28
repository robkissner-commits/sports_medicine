@echo off
REM Quick launcher - assumes setup is already done

REM Start backend
start "Sports Medicine - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python run_backend.py"

REM Wait 5 seconds
timeout /t 5 /nobreak > nul

REM Start frontend
start "Sports Medicine - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

REM Wait 3 seconds
timeout /t 3 /nobreak > nul

REM Open browser
start http://localhost:3000
