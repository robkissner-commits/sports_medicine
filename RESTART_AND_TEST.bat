@echo off
echo ========================================
echo COMPLETE RESTART
echo Sports Medicine System
echo ========================================
echo.
echo This will completely stop and restart the application.
echo.

echo [1/5] Stopping all running servers...
taskkill /FI "WindowTitle eq Sports Medicine - Backend*" /T /F 2>nul
taskkill /FI "WindowTitle eq Sports Medicine - Frontend*" /T /F 2>nul
echo Stopped all servers.

echo.
echo [2/5] Waiting for ports to be released...
timeout /t 3 /nobreak > nul
echo Ports should now be free.

echo.
echo [3/5] Starting Backend Server...
start "Sports Medicine - Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python run_backend.py"
echo Backend starting...

echo.
echo [4/5] Waiting for backend to initialize...
timeout /t 8 /nobreak > nul
echo Backend should be ready.

echo.
echo [5/5] Starting Frontend Server...
start "Sports Medicine - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo Frontend starting...

echo.
echo ========================================
echo Restart Complete!
echo ========================================
echo.
echo Waiting for frontend to be ready...
timeout /t 5 /nobreak > nul

echo.
echo Opening application in browser...
start http://127.0.0.1:3000/test
echo.
echo ========================================
echo IMPORTANT: Check the Connection Test page!
echo ========================================
echo.
echo The browser should open to a Connection Test page.
echo This will show you exactly what's working and what's not.
echo.
echo If all tests are GREEN: Everything is working!
echo If tests are RED: See the troubleshooting tips on the page.
echo.
pause
