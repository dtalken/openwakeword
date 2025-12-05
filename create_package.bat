@echo off
REM Create a deployment package for new Windows machines

echo ============================================
echo Creating deployment package...
echo ============================================
echo.

REM Create package directory
set PACKAGE_DIR=OpenWakeWord_Package
if exist %PACKAGE_DIR% rmdir /s /q %PACKAGE_DIR%
mkdir %PACKAGE_DIR%

REM Copy essential files
echo Copying files...
copy setup_windows.bat %PACKAGE_DIR%\
copy requirements-windows-fixed.txt %PACKAGE_DIR%\
copy patch_speechbrain.py %PACKAGE_DIR%\
copy fix_torchaudio_backend.py %PACKAGE_DIR%\
copy fix_trim_mmap.py %PACKAGE_DIR%\
copy apply_fixes.py %PACKAGE_DIR%\
copy train.bat %PACKAGE_DIR%\
copy train_config.yaml %PACKAGE_DIR%\
copy check_dataset.py %PACKAGE_DIR%\
copy normalize_audio.py %PACKAGE_DIR%\
copy prepare_data.py %PACKAGE_DIR%\
copy final_onnx_to_tflite.py %PACKAGE_DIR%\
copy test_model.py %PACKAGE_DIR%\
copy QUICK_START_NEW_MACHINE.txt %PACKAGE_DIR%\
copy SETUP_NEW_MACHINE.md %PACKAGE_DIR%\

REM Create dataset directories
mkdir %PACKAGE_DIR%\dataset
mkdir %PACKAGE_DIR%\dataset\positive
mkdir %PACKAGE_DIR%\dataset\negative
mkdir %PACKAGE_DIR%\models

echo.
echo ============================================
echo Package created: %PACKAGE_DIR%\
echo ============================================
echo.
echo Files ready to copy to new machine!
echo.
echo To use on new machine:
echo   1. Copy the entire "%PACKAGE_DIR%" folder
echo   2. Run: setup_windows.bat
echo   3. Add audio files to dataset\
echo   4. Run: train.bat
echo.
pause

