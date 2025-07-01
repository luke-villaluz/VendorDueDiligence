@echo off
echo ========================================
echo Vendor Due Diligence Tool
echo ========================================
echo.
echo Starting GUI application...
echo.
echo Features:
echo - Browse and select vendor folders
echo - Choose specific vendors or process all
echo - Automatic Ollama server management
echo - Real-time progress tracking
echo - Professional PDF reports saved in vendor folders
echo.
echo The GUI will automatically:
echo - Start Ollama server if needed
echo - Show vendor selection options
echo - Display processing progress
echo - Stop Ollama when you close the window
echo.
pause

REM Change to the parent directory (project root)
cd /d "%~dp0.."

REM Activate virtual environment if it exists
if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
)

python vendor_dd_gui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start the GUI application
    echo.
    echo Troubleshooting:
    echo 1. Make sure Python is installed (https://python.org)
    echo 2. Make sure Ollama is installed (https://ollama.ai)
    echo 3. Run windows\install.bat to set up dependencies
    echo 4. Check that vendor_dd_gui.py exists in this folder
    echo.
    pause
    exit /b 1
)

echo.
echo Application closed successfully.
pause 