#!/bin/bash

# Training wrapper script for OpenWakeWord

echo "=========================================="
echo "  OpenWakeWord Training Pipeline"
echo "=========================================="
echo ""

# Check if dataset exists
if [ ! -d "dataset/positive" ] || [ ! -d "dataset/negative" ]; then
    echo "❌ Error: Dataset directories not found!"
    echo "Please create dataset/positive and dataset/negative folders"
    exit 1
fi

# Step 1: Check dataset
echo "Step 1: Checking dataset..."
python3 check_dataset.py
echo ""
read -p "Does the dataset look good? Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Training cancelled. Please fix your dataset first."
    exit 1
fi

# Step 2: Normalize audio
echo ""
echo "Step 2: Normalizing audio files..."
python3 normalize_audio.py
echo ""

# Step 2.5: Prepare data structure (train/test split)
echo "Step 2.5: Preparing data structure..."
python3 prepare_data.py
echo ""

# Step 2.6: Apply training fixes
echo "Step 2.6: Applying training fixes..."
python3 apply_fixes.py
echo ""

# Step 3: Train model (with torchaudio compatibility fix)
echo "Step 3: Starting training..."
echo "This may take a while depending on your dataset size and hardware."
echo ""
python3 train_with_fixes.py --training_config train_config.yaml --augment_clips --overwrite --train_model

# Step 4: Convert ONNX to TFLite
echo ""
echo "Step 4: Converting ONNX to TFLite..."
if [ -f "models/hey_mel.onnx" ]; then
    python3 final_onnx_to_tflite.py
    if [ $? -eq 0 ]; then
        echo "✓ TFLite conversion successful"
    else
        echo "⚠️  TFLite conversion failed, but ONNX model is still available"
    fi
else
    echo "⚠️  ONNX model not found, skipping TFLite conversion"
fi
echo ""

# Step 5: Check if model was created
if [ -f "models/hey_mel.onnx" ]; then
    echo ""
    echo "=========================================="
    echo "✓ Training Complete!"
    echo "=========================================="
    echo ""
    echo "Your models are ready:"
    echo "  ✓ models/hey_mel.onnx (ONNX format)"
    echo ""
    if [ -f "models/hey_mel.tflite" ]; then
        echo "  ✓ models/hey_mel.tflite (TFLite format)"
        echo ""
        echo "Model sizes:"
        ls -lh models/hey_mel.onnx models/hey_mel.tflite
    else
        echo "  ⚠️  TFLite conversion was skipped or failed"
        echo ""
        echo "Model size:"
        ls -lh models/hey_mel.onnx
        echo ""
        echo "To convert to TFLite manually, run:"
        echo "  python3 final_onnx_to_tflite.py"
    fi
    echo ""
    echo "Next steps:"
    echo "  1. Test your model: python3 test_model.py <audio_file.wav>"
    echo "  2. Integrate into your application"
    echo "  3. Deploy to your target platform"
else
    echo ""
    echo "❌ Training failed or model not found!"
    echo "Check the error messages above."
fi

