@echo off
REM Training wrapper script for OpenWakeWord on Windows

echo ==========================================
echo   OpenWakeWord Training Pipeline
echo ==========================================
echo.

REM Check if dataset exists
if not exist "dataset\positive" (
    echo Error: dataset\positive directory not found!
    echo Please create dataset\positive and dataset\negative folders
    exit /b 1
)
if not exist "dataset\negative" (
    echo Error: dataset\negative directory not found!
    echo Please create dataset\positive and dataset\negative folders
    exit /b 1
)

REM Step 1: Check dataset
echo Step 1: Checking dataset...
python check_dataset.py
echo.
set /p REPLY="Does the dataset look good? Continue? (y/n): "
if /i not "%REPLY%"=="y" (
    echo Training cancelled. Please fix your dataset first.
    exit /b 1
)

REM Step 2: Normalize audio
echo.
echo Step 2: Normalizing audio files...
python normalize_audio.py
echo.

REM Step 2.5: Prepare data structure
echo Step 2.5: Preparing data structure...
python prepare_data.py
echo.

REM Step 2.6: Apply training fixes
echo Step 2.6: Applying training fixes...
python apply_fixes.py
echo.

REM Step 3: Train model
echo Step 3: Starting training...
echo This may take a while depending on your dataset size and hardware.
echo.
python -m openwakeword.train --training_config train_config.yaml --augment_clips --overwrite --train_model

REM Step 4: Convert ONNX to TFLite
echo.
echo Step 4: Converting ONNX to TFLite...
if exist "models\hey_mel.onnx" (
    python final_onnx_to_tflite.py
    if %ERRORLEVEL% EQU 0 (
        echo TFLite conversion successful
    ) else (
        echo TFLite conversion failed, but ONNX model is still available
    )
) else (
    echo ONNX model not found, skipping TFLite conversion
)
echo.

REM Step 5: Check if model was created
if exist "models\hey_mel.onnx" (
    echo.
    echo ==========================================
    echo Training Complete!
    echo ==========================================
    echo.
    echo Your models are ready:
    echo   -^> models\hey_mel.onnx (ONNX format)
    echo.
    if exist "models\hey_mel.tflite" (
        echo   -^> models\hey_mel.tflite (TFLite format)
        echo.
        echo Model sizes:
        dir models\hey_mel.onnx models\hey_mel.tflite
    ) else (
        echo   TFLite conversion was skipped or failed
        echo.
        echo Model size:
        dir models\hey_mel.onnx
        echo.
        echo To convert to TFLite manually, run:
        echo   python final_onnx_to_tflite.py
    )
    echo.
    echo Next steps:
    echo   1. Test your model: python test_model.py ^<audio_file.wav^>
    echo   2. Integrate into your application
    echo   3. Deploy to your target platform
) else (
    echo.
    echo Training failed or model not found!
    echo Check the error messages above.
)

echo.
pause

