@echo off
echo ========================================
echo Creating Desktop Shortcut
echo ========================================
echo.

REM Get the absolute path to the batch file
set "BATCH_PATH=%~dp0Run_Vendor_DD.bat"
REM Remove trailing backslash if present
if "%BATCH_PATH:~-1%"=="\" set "BATCH_PATH=%BATCH_PATH:~0,-1%"
set "BATCH_FILE=%BATCH_PATH%"

REM Get the user's desktop path
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do set "DESKTOP=%%b"

if not defined DESKTOP (
    echo ERROR: Could not find desktop path
    pause
    exit /b 1
)

REM Create the shortcut
echo Creating shortcut on desktop...
echo Target: %BATCH_FILE%
echo Desktop: %DESKTOP%

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Vendor Due Diligence Tool.lnk'); $Shortcut.TargetPath = '%BATCH_FILE%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Vendor Due Diligence Automation Tool'; $Shortcut.Save()"

if errorlevel 1 (
    echo ERROR: Failed to create shortcut
    pause
    exit /b 1
)

echo.
echo ========================================
echo Shortcut Created Successfully!
echo ========================================
echo.
echo A shortcut named "Vendor Due Diligence Tool" has been created on your desktop.
echo You can now double-click it to run the tool from anywhere.
echo.
pause 