@echo off
echo Stopping Sports Medicine Application...
echo.

REM Kill any running Python processes (backend)
taskkill /FI "WindowTitle eq Sports Medicine - Backend*" /T /F 2>nul

REM Kill any running Node processes (frontend)
taskkill /FI "WindowTitle eq Sports Medicine - Frontend*" /T /F 2>nul

echo.
echo Application stopped.
echo.
pause
