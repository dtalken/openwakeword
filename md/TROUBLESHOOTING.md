# 🔧 Troubleshooting Guide

## Issue 1: Architecture Mismatch (Apple Silicon)

### Error:
```
ImportError: mach-o file, but is an incompatible architecture 
(have 'x86_64', need 'arm64e' or 'arm64')
```

### Cause:
You're on an Apple Silicon (M1/M2/M3) Mac, but packages were installed for Intel architecture.

### Solution:
Run the setup script:
```bash
bash setup_environment.sh
```

Or see `INSTALL_FIX.md` for detailed instructions.

---

## Issue 2: "No module named openwakeword-train"

### Error:
```
No module named openwakeword-train
```

### Cause:
The command `openwakeword-train` doesn't exist. The correct syntax is different.

### Solution:
Use this command instead:
```bash
python3 -m openwakeword.train --config train_config.yaml
```

All scripts have been updated to use the correct command.

---

## Issue 3: OpenWakeWord Not Installed

### Error:
```
ModuleNotFoundError: No module named 'openwakeword'
```

### Solution:
Install dependencies:
```bash
pip3 install -r requirements.txt
```

Or install individually:
```bash
pip3 install openwakeword torch torchaudio onnx onnxruntime pydub numpy audiomentations chardet librosa soundfile scipy
```

---

## Issue 3b: Missing audiomentations

### Error:
```
ModuleNotFoundError: No module named 'audiomentations'
```

### Cause:
OpenWakeWord requires `audiomentations` for data augmentation during training.

### Solution:
```bash
pip3 install audiomentations chardet librosa soundfile scipy
```

Or use the quick fix script:
```bash
bash install_missing_deps.sh
```

---

## Issue 3c: Torchaudio Compatibility Error

### Error:
```
AttributeError: module 'torchaudio' has no attribute 'list_audio_backends'
```

### Cause:
SpeechBrain 1.0.3 expects `torchaudio.list_audio_backends()` which doesn't exist in some torchaudio versions (like 2.2.2 or 2.9.1+cpu).

### Solution:
**Option 1: Use the training wrapper (Recommended)**
```bash
# Windows
python train_with_fixes.py --training_config train_config.yaml --augment_clips --overwrite --train_model

# Linux/Mac
python3 train_with_fixes.py --training_config train_config.yaml --augment_clips --overwrite --train_model
```

**Option 2: Apply fix manually before training**
```python
# In your Python script, import the fix FIRST:
import fix_torchaudio_compat  # This patches torchaudio automatically
# Now you can import speechbrain or openwakeword safely
from openwakeword import train
```

**Option 3: Run the fix script**
```bash
python fix_torchaudio_compat.py
# Then run your training command normally
```

The fix automatically adds the missing `list_audio_backends()` function to torchaudio.

---

## Issue 4: Training Fails - Dataset Issues

### Error:
```
FileNotFoundError: [Errno 2] No such file or directory: 'dataset/positive'
```

### Solution:
Make sure your dataset structure is correct:
```
dataset/
  ├── positive/     ← Wake word samples
  │   ├── sample1.wav
  │   ├── sample2.wav
  │   └── ...
  └── negative/     ← Background noise
      ├── noise1.wav
      ├── noise2.wav
      └── ...
```

Check with:
```bash
python3 check_dataset.py
```

---

## Issue 5: Audio Format Issues

### Error:
```
Error processing audio file
```

### Cause:
Audio files not in correct format.

### Solution:
Run normalization:
```bash
python3 normalize_audio.py
```

This converts all files to: 16kHz, mono, PCM16

---

## Issue 6: Permission Errors

### Error:
```
PermissionError: [Errno 1] Operation not permitted
```

### Solution:
- Don't use `sudo` with pip
- Use a virtual environment instead:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Issue 7: Model Not Found After Training

### Error:
```
Model file not found: models/hey_mel.tflite
```

### Cause:
Training didn't complete successfully or output directory issue.

### Solution:
1. Check if training completed without errors
2. Look for the model file:
   ```bash
   ls -lh models/
   ```
3. Check training logs for errors
4. Make sure `wakeword_name` in `train_config.yaml` matches

---

## Issue 8: Out of Memory During Training

### Error:
```
RuntimeError: CUDA out of memory
```
or
```
Killed
```

### Solution:
Reduce batch size in `train_config.yaml`:
```yaml
batch_size: 16  # or even 8
```

---

## Issue 9: Training Takes Too Long

### Not an error, but slow training

### Solutions:
1. **Reduce dataset size** (start with 50 positive + 100 negative)
2. **Reduce epochs** in `train_config.yaml`:
   ```yaml
   epochs: 20
   ```
3. **Use GPU** if available
4. **Reduce batch size** (counterintuitively, smaller batches = faster per-epoch)

---

## Issue 10: Model Accuracy Poor

### Model detects everything / nothing

### Solutions:

**Too many false positives:**
- Add more negative samples
- Increase detection threshold in app (0.7 instead of 0.5)
- Add more diverse negative samples

**Misses real wake words:**
- Add more positive samples with variations
- Lower detection threshold (0.4 instead of 0.5)
- Record samples in realistic conditions
- Increase epochs to 60-80

**General improvement:**
- More diverse training data
- Different speakers
- Different environments
- Different volumes/distances

---

## Issue 11: Virtual Environment Issues

### Can't activate venv or packages not found

### Solution:
```bash
# Deactivate if already in a venv
deactivate

# Remove old venv
rm -rf venv

# Create fresh venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Issue 12: Test Script Fails

### Error when running test_model.py

### Solution:
Make sure model exists:
```bash
ls models/hey_mel.tflite
```

If not, train first:
```bash
bash train.sh
```

---

## Quick Diagnostic Commands

```bash
# Check Python version
python3 --version

# Check if OpenWakeWord is installed
python3 -c "import openwakeword; print(openwakeword.__version__)"

# Check numpy architecture
python3 -c "import numpy; print(numpy.__version__)"

# Check dataset
python3 check_dataset.py

# List installed packages
pip3 list | grep -E "openwakeword|numpy|torch"

# Check file structure
ls -R dataset/
ls -lh models/
```

---

## Still Having Issues?

1. **Read the error message carefully** - it usually tells you what's wrong
2. **Check `INSTALL_FIX.md`** for architecture issues
3. **Run diagnostic commands** above
4. **Start fresh** with a virtual environment:
   ```bash
   bash setup_environment.sh
   ```

---

## Common Command Reference

```bash
# Setup environment (fixes most issues)
bash setup_environment.sh

# Check dataset
python3 check_dataset.py

# Normalize audio
python3 normalize_audio.py

# Train model
python3 -m openwakeword.train --config train_config.yaml

# Test model
python3 test_model.py dataset/positive/sample.wav

# Automated training
bash train.sh
```

