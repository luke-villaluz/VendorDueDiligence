@echo off
echo ========================================
echo Vendor Due Diligence Tool - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

REM Check if virtual environment exists
if not exist "env\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv env
)

REM Activate virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat

REM Install requirements if needed
REM if not exist "env\Lib\site-packages\openpyxl" (
REM     echo Installing required packages...
REM     pip install -r config\requirements.txt
REM ) else (
REM     echo Required packages already installed.
REM )

REM Instead, always install requirements
pip install -r config\requirements.txt

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Ollama is not installed or not in PATH
    echo Please install Ollama from https://ollama.ai
    echo The GUI will attempt to start Ollama automatically, but manual installation is recommended
    echo.
) else (
    echo Ollama found. Checking version...
    ollama --version
)

echo.
echo ========================================
echo Creating Desktop Shortcut...
echo ========================================
call "%~dp0Create_Desktop_Shortcut.bat"

echo.
echo ========================================
echo Installation and shortcut creation complete!
echo ========================================
echo.
echo You can now double-click the "Vendor Due Diligence Tool" shortcut on your desktop to run the app.
echo.
echo To run the tool:
echo 1. Double-click windows\Run_Vendor_DD.bat
echo 2. Or run: python vendor_dd_gui.py
echo.
echo For help, see USER_GUIDE.md
echo.
pause 