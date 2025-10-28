@echo off
echo ========================================
echo Network Troubleshooting
echo Sports Medicine System
echo ========================================
echo.
echo Testing backend connection...
echo.

echo [1] Checking if backend is accessible...
curl -s http://localhost:8000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend is running on http://localhost:8000
) else (
    echo ✗ Backend not accessible on http://localhost:8000
)

curl -s http://127.0.0.1:8000 > nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend is running on http://127.0.0.1:8000
) else (
    echo ✗ Backend not accessible on http://127.0.0.1:8000
)

echo.
echo [2] Checking if ports are in use...
netstat -ano | findstr :8000 > nul
if %errorlevel% equ 0 (
    echo ✓ Port 8000 is in use (backend should be running)
    netstat -ano | findstr :8000
) else (
    echo ✗ Port 8000 is NOT in use (backend may not be running)
)

echo.
netstat -ano | findstr :3000 > nul
if %errorlevel% equ 0 (
    echo ✓ Port 3000 is in use (frontend should be running)
    netstat -ano | findstr :3000
) else (
    echo ✗ Port 3000 is NOT in use (frontend may not be running)
)

echo.
echo ========================================
echo Recommendations:
echo ========================================
echo.

echo If backend is NOT running:
echo   1. Close all terminal windows
echo   2. Run START_APP.bat again
echo.

echo If ports show as in use but apps not working:
echo   1. Run STOP_APP.bat
echo   2. Wait 5 seconds
echo   3. Run START_APP.bat again
echo.

echo If still having issues:
echo   1. Restart your computer
echo   2. Check Windows Firewall settings
echo   3. Make sure Python and Node.js are installed
echo.

pause
