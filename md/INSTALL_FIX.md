# 🔧 Installation Fix for Apple Silicon Macs

## The Problem

You're getting this error:
```
ImportError: dlopen(...numpy...): mach-o file, but is an incompatible architecture 
(have 'x86_64', need 'arm64e' or 'arm64')
```

**This means**: Your Python packages (numpy, etc.) were installed for Intel Macs, but you have an Apple Silicon (M1/M2/M3) Mac.

## The Solution

You need to reinstall everything with the correct architecture. Here are **3 options**:

---

## ✅ Option 1: Clean Reinstall (RECOMMENDED)

This will fix the architecture issue completely.

```bash
# 1. Uninstall existing packages
pip3 uninstall -y numpy torch torchaudio openwakeword onnx onnxruntime pydub

# 2. Clear pip cache
pip3 cache purge

# 3. Reinstall with correct architecture
pip3 install --no-cache-dir numpy
pip3 install --no-cache-dir torch torchaudio
pip3 install --no-cache-dir openwakeword onnx onnxruntime pydub

# 4. Verify installation
python3 -c "import numpy; import openwakeword; print('✓ Installation successful!')"
```

---

## ✅ Option 2: Use Virtual Environment (CLEANEST)

This creates a fresh environment with the correct architecture.

```bash
cd /Users/mac-obs-49/Desktop/train-tflite

# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install requirements
pip install -r requirements.txt

# 5. Verify
python -c "import numpy; import openwakeword; print('✓ Installation successful!')"

# 6. Run training (while venv is activated)
bash train.sh
```

**Important**: Always activate the venv before working:
```bash
source venv/bin/activate
```

---

## ✅ Option 3: Use Rosetta 2 (SLOWER, NOT RECOMMENDED)

If options 1 & 2 don't work, you can run Python in Intel emulation mode:

```bash
# Run Python in x86 mode
arch -x86_64 python3 -m pip install numpy torch torchaudio openwakeword
```

---

## 🧪 Test the Fix

After fixing, run this to confirm everything works:

```bash
python3 << EOF
import numpy as np
import openwakeword
print("NumPy version:", np.__version__)
print("OpenWakeWord version:", openwakeword.__version__)
print("✓ All dependencies working!")
EOF
```

---

## 🚀 After Fixing

Once installed correctly, the training command should be:

```bash
# NOT this (this doesn't exist):
openwakeword-train --config train_config.yaml

# Use this instead:
python3 -m openwakeword.train --config train_config.yaml
```

I'll update the training scripts to use the correct command.

