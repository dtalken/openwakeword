@echo off
REM ============================================
REM OpenWakeWord Training Setup for Windows
REM One-command setup - installs everything
REM ============================================

echo ============================================
echo OpenWakeWord Training Setup for Windows
echo ============================================
echo.
echo This will install all dependencies and apply patches.
echo Estimated time: 5-10 minutes
echo.
pause

REM Step 1: Upgrade pip
echo.
echo [1/6] Upgrading pip...
python -m pip install --upgrade pip

REM Step 2: Install core dependencies with specific versions
echo.
echo [2/6] Installing dependencies (this may take a few minutes)...
pip install torch==2.6.0 torchaudio==2.6.0
pip install torchmetrics pronouncing audiomentations torch-audiomentations
pip install mutagen acoustics matplotlib
pip install openwakeword speechbrain
pip install pydub scipy librosa soundfile
pip install onnx onnxruntime

REM Step 3: Download OpenWakeWord resources
echo.
echo [3/6] Downloading OpenWakeWord resources...
python -c "from openwakeword.utils import download_models; download_models()"

REM Step 4: Apply compatibility patches
echo.
echo [4/6] Applying compatibility patches...
python patch_speechbrain.py
python fix_torchaudio_backend.py
python fix_trim_mmap.py
python apply_fixes.py

REM Step 5: Verify installation
echo.
echo [5/6] Verifying installation...
python -c "from openwakeword import train; print('[OK] OpenWakeWord imports successfully')"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Installation verification failed
    pause
    exit /b 1
)

REM Step 6: Setup complete
echo.
echo [6/6] Setup complete!
echo.
echo ============================================
echo [SUCCESS] Installation Complete!
echo ============================================
echo.
echo Next steps:
echo   1. Add your audio files to dataset\positive and dataset\negative
echo   2. Run: train.bat
echo   3. Test: python test_model.py dataset\positive\sample.wav
echo.
echo ============================================
pause

