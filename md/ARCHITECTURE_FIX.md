# 🔧 Architecture Conflict Fix

## The Problem

You're experiencing a **mixed architecture** conflict:

```
ImportError: mach-o file, but is an incompatible architecture 
(have 'arm64', need 'x86_64')
```

This is the **opposite** of the earlier error. This means:
- Some packages are compiled for **ARM64** (Apple Silicon native)
- Some packages are compiled for **x86_64** (Intel/Rosetta)
- Python might be running under Rosetta while installing ARM64 packages (or vice versa)

This creates incompatible package combinations.

---

## Root Cause

This typically happens when:

1. **Python itself is x86_64** (installed for Intel or running under Rosetta)
2. **Some pip packages install ARM64 versions** (native wheels)
3. **They can't work together**

Or the reverse:
1. **Python is ARM64** (native Apple Silicon)
2. **Some packages only available as x86_64**
3. **Conflict occurs**

---

## ✅ Solution: Clean Virtual Environment

The **only reliable fix** is a clean virtual environment with consistent architecture.

### Run This Script:

```bash
bash fix_architecture.sh
```

This will:
1. ✓ Detect your architecture
2. ✓ Remove any old virtual environment
3. ✓ Create a fresh venv
4. ✓ Install ALL packages with consistent architecture
5. ✓ Test the installation
6. ✓ Create activation helper

**Time required:** 5-10 minutes (downloads packages)

---

## Manual Alternative

If the script doesn't work, do this manually:

```bash
cd /Users/mac-obs-49/Desktop/train-tflite

# Remove old venv
rm -rf venv

# Create fresh venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Verify architecture
python -c "import platform; print(platform.machine())"

# Upgrade pip
pip install --upgrade pip

# Install everything fresh
pip install --no-cache-dir numpy scipy
pip install --no-cache-dir librosa soundfile pydub
pip install --no-cache-dir audiomentations chardet
pip install --no-cache-dir torch torchaudio
pip install --no-cache-dir onnx onnxruntime
pip install --no-cache-dir openwakeword

# Test
python -c "import openwakeword; print('✓ Success!')"
```

---

## After Fixing

Once the environment is set up:

### 1. Always Activate First

```bash
source venv/bin/activate
```

Or use the helper:
```bash
source activate.sh
```

### 2. Run Training

```bash
bash train.sh
```

### 3. When Done, Deactivate

```bash
deactivate
```

---

## If Python Itself is the Problem

If the script warns that Python is running under Rosetta:

### Option A: Install Native ARM64 Python (Recommended)

```bash
# Using Homebrew
brew install python@3.11

# Then use it
/opt/homebrew/bin/python3 -m venv venv
```

### Option B: Force Consistent x86_64 Mode

```bash
# Start x86_64 shell
arch -x86_64 /bin/bash

# Verify
uname -m  # Should show x86_64

# Now run the fix script
bash fix_architecture.sh
```

Everything will be x86_64 (slower, but consistent).

---

## Verification

After setup, verify everything is consistent:

```bash
source venv/bin/activate

python << 'EOF'
import platform
import numpy
import torch
import openwakeword

print(f"Python arch: {platform.machine()}")
print(f"NumPy: {numpy.__version__}")
print(f"PyTorch: {torch.__version__}")
print(f"OpenWakeWord: {openwakeword.__version__}")
print("✅ All working!")
EOF
```

Should complete without errors.

---

## Why Virtual Environment?

A virtual environment:
- ✓ Isolates packages from system Python
- ✓ Ensures all packages use same architecture
- ✓ Prevents conflicts with other projects
- ✓ Easy to delete and recreate if issues arise
- ✓ No need for sudo/admin rights

This is the **standard best practice** for Python projects.

---

## Quick Reference

```bash
# Fix architecture issues
bash fix_architecture.sh

# Activate environment (do this every time)
source venv/bin/activate

# Train model
bash train.sh

# Deactivate when done
deactivate
```

---

## Troubleshooting

**"Still getting architecture errors"**
- Make sure you activated the venv: `source venv/bin/activate`
- Check prompt shows `(venv)` at the start
- Verify Python location: `which python` should show `.../venv/bin/python`

**"Script fails during installation"**
- Check internet connection
- Try manual installation steps above
- Consider using Homebrew Python: `brew install python@3.11`

**"Want to start completely fresh"**
```bash
rm -rf venv
bash fix_architecture.sh
```

---

**This is the definitive fix for the architecture conflict.** 🎯

