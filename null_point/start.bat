@echo off
set "TARGET_DIR=%~dp0"

echo Changing directory to: "%TARGET_DIR%"
cd /d "%TARGET_DIR%"

echo Starting Null Point...
if exist "null_point.py" (
    python null_point.py
) else (
    echo Error: null_point.py not found in "%TARGET_DIR%"
    pause
)

echo.
echo Script has ended. Press any key to close.
pause
