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
REM Auto-continue without interactive prompt (for non-interactive runs)
REM Previously this script asked: "Does the dataset look good? Continue? (y/n): "
REM If you need manual confirmation, reintroduce a prompt here.

REM Step 2: Normalize audio
echo.
echo Step 2: Normalizing audio files...
python normalize_audio.py
echo.

REM Step 2.5: Prepare data structure
echo Step 2.5: Preparing data structure...
python prepare_data.py
echo.

REM Step 2.6: Download OpenWakeWord resources
echo Step 2.6: Downloading OpenWakeWord resources...
python -c "from openwakeword.utils import download_models; download_models()"
echo.

REM Step 2.7: Fix torchaudio backend
echo Step 2.7: Fixing torchaudio backend...
python fix_torchaudio_backend.py
echo.

REM Step 2.8: Fix Windows file locking
echo Step 2.8: Fixing Windows file locking...
python fix_trim_mmap.py
echo.

REM Step 2.9: Apply SpeechBrain compatibility patch
echo Step 2.9: Applying SpeechBrain compatibility patch...
python patch_speechbrain.py
echo.

REM Step 2.10: Apply training fixes
echo Step 2.10: Applying training fixes...
python apply_fixes.py
echo.

REM Step 3: Train model
echo Step 3: Starting training...
echo This may take a while depending on your dataset size and hardware.
echo.
python -m openwakeword.train --training_config train_config.yaml --augment_clips --overwrite --train_model

REM Step 4: Convert ONNX to TFLite (Note: train.py already does this, but we run again to be sure)
echo.
echo Step 4: Verifying TFLite conversion...
if exist "models\hey_mel.onnx" (
    if exist "models\hey_mel.tflite" (
        echo ^>^> TFLite model already created by training process
    ) else (
        echo Converting ONNX to TFLite...
        python final_onnx_to_tflite.py
        if %ERRORLEVEL% EQU 0 (
            echo ^>^> TFLite conversion successful
        ) else (
            echo ^>^> TFLite conversion failed, but ONNX model is available
        )
    )
) else (
    echo ^>^> ONNX model not found, skipping TFLite conversion
)
echo.

REM Step 5: Check if model was created
echo.
if exist "models\hey_mel.onnx" (
    echo ==========================================
    echo ^>^>^> Training SUCCEEDED! ^<^<^<
    echo ==========================================
    echo.
    echo Your models are ready:
    echo   ^>^> models\hey_mel.onnx ^(ONNX format^)
    if exist "models\hey_mel.tflite" (
        echo   ^>^> models\hey_mel.tflite ^(TFLite format^)
    )
    echo.
    echo Model sizes:
    for %%F in (models\hey_mel.onnx models\hey_mel.tflite) do (
        if exist "%%F" (
            echo   %%~nxF: %%~zF bytes
        )
    )
    echo.
    echo Next steps:
    echo   1. Test your model: python test_model.py dataset\positive\HeyMel_TalkenDan_2025-11-04_1.wav
    echo   2. Add more training samples for better accuracy ^(currently only 5+5 samples^)
    echo   3. Integrate into your application
    echo   4. Deploy to your target platform
    echo.
    echo ==========================================
    goto :end
)

echo ==========================================
echo ^>^>^> Training FAILED! ^<^<^<
echo ==========================================
echo ONNX model not found at models\hey_mel.onnx
echo Check the error messages above.
echo.

:end

echo.
pause

