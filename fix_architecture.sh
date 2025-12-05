#!/bin/bash

# ====================================================
# COMPLETE ARCHITECTURE FIX FOR APPLE SILICON
# Resolves mixed x86_64/arm64 package conflicts
# ====================================================

echo "=============================================="
echo "  Architecture Fix for OpenWakeWord"
echo "=============================================="
echo ""

# Check current architecture
echo "Current system architecture: $(uname -m)"
echo "Current Python: $(which python3)"
echo "Python architecture: $(python3 -c 'import platform; print(platform.machine())')"
echo ""

# Detect if Python is running under Rosetta
PYTHON_ARCH=$(python3 -c 'import platform; print(platform.machine())')

if [[ "$PYTHON_ARCH" == "x86_64" ]] && [[ "$(uname -m)" == "arm64" ]]; then
    echo "⚠️  WARNING: Python is running under Rosetta (x86_64 on ARM64 system)"
    echo "This causes architecture conflicts."
    echo ""
    echo "SOLUTION 1: Use native ARM64 Python"
    echo "  Install Python from python.org or use Homebrew:"
    echo "  brew install python@3.11"
    echo ""
    echo "SOLUTION 2: Force everything to x86_64 mode (slower)"
    echo "  arch -x86_64 /bin/bash"
    echo "  Then run this script again"
    echo ""
    read -p "Continue with current Python anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Creating clean virtual environment..."
echo "=============================================="

# Remove old venv if it exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate it
echo "Activating virtual environment..."
source venv/bin/activate

# Verify architecture
echo ""
echo "Virtual environment Python architecture:"
python -c 'import platform; print(platform.machine())'

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install wheel and setuptools first
echo ""
echo "Installing build tools..."
pip install wheel setuptools

# Install packages one by one to catch errors
echo ""
echo "Installing dependencies (this may take 5-10 minutes)..."
echo "=============================================="

# Core packages first
echo "→ Installing numpy (version 1.x for PyTorch compatibility)..."
pip install --no-cache-dir "numpy<2"

echo "→ Installing scipy..."
pip install --no-cache-dir scipy

echo "→ Installing audio processing libraries..."
pip install --no-cache-dir librosa soundfile

echo "→ Installing pydub..."
pip install --no-cache-dir pydub

echo "→ Installing audiomentations..."
pip install --no-cache-dir audiomentations "numpy<2"

echo "→ Installing chardet..."
pip install --no-cache-dir chardet

echo "→ Installing PyTorch (this may take a while)..."
pip install --no-cache-dir torch torchaudio "numpy<2"

echo "→ Installing ONNX..."
pip install --no-cache-dir onnx onnxruntime "numpy<2"

echo "→ Installing OpenWakeWord..."
pip install --no-cache-dir openwakeword "numpy<2"

echo "→ Installing training dependencies..."
pip install --no-cache-dir torchinfo torchmetrics pyyaml pronouncing torch-audiomentations speechbrain mutagen acoustics matplotlib "numpy<2"

echo ""
echo "=============================================="
echo "Testing installation..."
echo "=============================================="

python << 'EOF'
import sys
print(f"Python: {sys.version}")

try:
    import platform
    print(f"Architecture: {platform.machine()}")
    
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
    
    import scipy
    print(f"✓ SciPy {scipy.__version__}")
    
    import librosa
    print(f"✓ Librosa {librosa.__version__}")
    
    import soundfile
    print(f"✓ SoundFile {soundfile.__version__}")
    
    import audiomentations
    print(f"✓ Audiomentations {audiomentations.__version__}")
    
    import torch
    print(f"✓ PyTorch {torch.__version__}")
    
    import openwakeword
    try:
        print(f"✓ OpenWakeWord {openwakeword.__version__}")
    except AttributeError:
        print(f"✓ OpenWakeWord (installed)")
    
    print("\n✅ All dependencies installed successfully!")
    print("All packages are using the same architecture.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "=============================================="
    echo "✅ SUCCESS! Environment is ready."
    echo "=============================================="
    echo ""
    echo "IMPORTANT: Always activate the virtual environment before working:"
    echo ""
    echo "  source venv/bin/activate"
    echo ""
    echo "Then run training:"
    echo "  bash train.sh"
    echo ""
    echo "To deactivate when done:"
    echo "  deactivate"
    echo ""
    
    # Create activation helper
    cat > activate.sh << 'ACTIVATE'
#!/bin/bash
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "Run: bash train.sh"
ACTIVATE
    chmod +x activate.sh
    
    echo "Quick activation script created: ./activate.sh"
    echo ""
else
    echo ""
    echo "❌ Installation failed. Please check errors above."
    exit 1
fi


