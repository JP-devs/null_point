@echo off
set "TARGET_DIR=%~dp0"

echo Changing directory to: "%TARGET_DIR%"
cd /d "%TARGET_DIR%"

echo Updating pip...
python -m pip install --upgrade pip

echo Installing core dependencies...
python -m pip install -r requirements.txt

echo Installation complete.
echo.
echo You can now start the framework using start.bat
pause
