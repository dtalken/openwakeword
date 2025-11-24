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

# Step 3: Train model
echo "Step 3: Starting training..."
echo "This may take a while depending on your dataset size and hardware."
echo ""
python3 -m openwakeword.train --config train_config.yaml

# Step 4: Check if model was created
if [ -f "models/hey_mel.tflite" ]; then
    echo ""
    echo "=========================================="
    echo "✓ Training Complete!"
    echo "=========================================="
    echo ""
    echo "Your model is ready:"
    echo "  → models/hey_mel.tflite"
    echo ""
    echo "Next steps:"
    echo "  1. Test: python test_model.py <audio_file.wav>"
    echo "  2. Copy models/hey_mel.tflite to your Flutter app"
    echo "  3. Follow Flutter integration steps in README.md"
else
    echo ""
    echo "❌ Training failed or model not found!"
    echo "Check the error messages above."
fi

