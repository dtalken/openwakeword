@echo off
REM Activate virtual environment for Windows

echo ==========================================
echo   Activating Virtual Environment
echo ==========================================
echo.

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo.
    echo Virtual environment activated!
    echo.
    echo Python version:
    python --version
    echo.
    echo Pip version:
    pip --version
    echo.
    echo ==========================================
    echo Ready to train! Run: train.bat
    echo ==========================================
    echo.
    echo To deactivate, type: deactivate
) else (
    echo Error: Virtual environment not found!
    echo Please create it first: python -m venv venv
    exit /b 1
)

