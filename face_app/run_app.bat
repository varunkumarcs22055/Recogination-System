@echo off
REM Face Recognition System - Quick Launcher for Windows
REM This script activates the virtual environment and runs the app

echo ========================================
echo Face Recognition System Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please create it first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import face_recognition" 2>nul
if errorlevel 1 (
    echo ERROR: Dependencies not installed!
    echo.
    echo Please install them:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo Starting Face Recognition System...
echo Web interface will open at: http://127.0.0.1:7860
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the application
python app_perfect.py

pause
