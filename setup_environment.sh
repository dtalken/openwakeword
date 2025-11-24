#!/bin/bash

# ====================================
# Setup Script for OpenWakeWord Training
# Fixes Apple Silicon architecture issues
# ====================================

echo "=========================================="
echo "  OpenWakeWord Environment Setup"
echo "=========================================="
echo ""

# Detect if running on Apple Silicon
if [[ $(uname -m) == 'arm64' ]]; then
    echo "✓ Detected: Apple Silicon (ARM64) Mac"
    APPLE_SILICON=true
else
    echo "✓ Detected: Intel (x86_64) Mac"
    APPLE_SILICON=false
fi

echo ""
echo "Choose installation method:"
echo "  1) Virtual Environment (recommended - cleanest)"
echo "  2) Global reinstall (fixes architecture issues)"
echo "  3) Skip (packages already installed correctly)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Creating virtual environment..."
        python3 -m venv venv
        
        echo "Activating virtual environment..."
        source venv/bin/activate
        
        echo "Upgrading pip..."
        pip install --upgrade pip
        
        echo "Installing requirements..."
        pip install --no-cache-dir -r requirements.txt
        
        echo ""
        echo "=========================================="
        echo "✓ Virtual Environment Setup Complete!"
        echo "=========================================="
        echo ""
        echo "IMPORTANT: Always activate the environment before working:"
        echo "  source venv/bin/activate"
        echo ""
        echo "To train your model:"
        echo "  source venv/bin/activate"
        echo "  bash train.sh"
        echo ""
        ;;
        
    2)
        echo ""
        echo "Uninstalling existing packages..."
        pip3 uninstall -y numpy torch torchaudio openwakeword onnx onnxruntime pydub 2>/dev/null
        
        echo "Clearing pip cache..."
        pip3 cache purge
        
        echo "Installing packages with correct architecture..."
        pip3 install --no-cache-dir numpy
        pip3 install --no-cache-dir torch torchaudio
        pip3 install --no-cache-dir openwakeword onnx onnxruntime pydub
        
        echo ""
        echo "=========================================="
        echo "✓ Global Installation Complete!"
        echo "=========================================="
        ;;
        
    3)
        echo ""
        echo "Skipping installation..."
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Test installation
echo ""
echo "Testing installation..."
python3 << 'EOF'
try:
    import numpy as np
    import openwakeword
    print("✓ NumPy version:", np.__version__)
    print("✓ OpenWakeWord version:", openwakeword.__version__)
    print("\n✅ All dependencies installed correctly!")
except Exception as e:
    print("\n❌ Error:", str(e))
    print("\nPlease check INSTALL_FIX.md for troubleshooting.")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "🎉 Setup Complete! You're ready to train."
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  1. Add WAV files to dataset/positive/ and dataset/negative/"
    echo "  2. Run: bash train.sh"
    echo ""
fi


