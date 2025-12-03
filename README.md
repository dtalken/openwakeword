# OpenWakeWord Training Pipeline

Complete training pipeline for custom wake word detection models using OpenWakeWord.

**Status:** ✅ Fully Functional | **Platform:** macOS, Windows, Linux | **Python:** 3.12+

---

## 🚀 Quick Start

### macOS/Linux:
```bash
cd train-tflite
source venv/bin/activate  # or: source activate.sh
./train.sh
```

### Windows:
```cmd
cd train-tflite
venv\Scripts\activate.bat  REM or: activate.bat
train.bat
```

---

## 📁 Project Structure

```
train-tflite/
├── README.md                    ← You are here
├── WINDOWS_SETUP.md            ← Complete Windows guide
├── TRAINING_SUCCESS.md         ← Training details & results
├── requirements.txt            ← All dependencies (120 packages)
├── requirements-core.txt       ← Core dependencies only
│
├── train.sh                    ← Training script (Mac/Linux)
├── train.bat                   ← Training script (Windows)
├── activate.sh                 ← Activate venv (Mac/Linux)
├── activate.bat                ← Activate venv (Windows)
│
├── check_dataset.py            ← Validate dataset
├── normalize_audio.py          ← Audio preprocessing
├── prepare_data.py             ← Train/test split
├── apply_fixes.py              ← Apply OpenWakeWord patches
├── train_config.yaml           ← Training configuration
│
├── dataset/                    ← Your audio files
│   ├── positive/              ← Wake word recordings
│   └── negative/              ← Background noise/other speech
│
├── models/                     ← Output directory
│   └── hey_mel.onnx           ← Trained model (after training)
│
└── venv/                       ← Virtual environment
```

---

## 📋 Prerequisites

### All Platforms:
- Python 3.12+
- 4GB+ RAM
- 2GB+ disk space

### Windows-Specific:
- Visual Studio Build Tools
- FFmpeg

### macOS-Specific:
- Xcode Command Line Tools
- Homebrew (recommended)

**See `WINDOWS_SETUP.md` for detailed Windows instructions.**

---

## 🎯 Setup Instructions

### 1. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Dataset

Add audio files to:
- `dataset/positive/` - Your wake word (e.g., "Hey Mel")
- `dataset/negative/` - Background noise, other speech

**Minimum:** 5 positive + 5 negative  
**Recommended:** 50-200 positive + 100-500 negative

### 4. Run Training

**macOS/Linux:**
```bash
./train.sh
```

**Windows:**
```cmd
train.bat
```

---

## ⚙️ Configuration

Edit `train_config.yaml` to customize:

```yaml
model_name: "hey_mel"           # Your model name
target_phrase: "hey mel"        # Your wake word
steps: 500                      # Training steps
layer_size: 96                  # Model complexity
total_length: 42000             # Audio length (samples)
```

---

## 📊 Training Process

The training script automatically:

1. ✅ **Validates** dataset structure and counts files
2. ✅ **Normalizes** audio to 16kHz, mono, PCM16
3. ✅ **Splits** data into train/test sets (80/20)
4. ✅ **Applies** necessary bug fixes to OpenWakeWord
5. ✅ **Augments** audio with variations
6. ✅ **Trains** model with specified configuration
7. ✅ **Exports** trained model to ONNX format

**Expected Time:** 2-30 minutes (depending on dataset size)

---

## 🎉 Output

After successful training:

```
models/hey_mel.onnx    (~618 KB)
```

**Format:** ONNX (Open Neural Network Exchange)  
**Use with:** ONNX Runtime, TensorFlow, PyTorch, mobile apps

---

## 🐛 Troubleshooting

### Dataset Issues:
```bash
python check_dataset.py
```

### Training Fails:
1. Check you have minimum 5+5 audio files
2. Ensure virtual environment is activated
3. Verify all dependencies installed
4. Check available disk space (2GB+)

### Windows-Specific Issues:
See `WINDOWS_SETUP.md` for detailed troubleshooting.

### Common Error: "mapping" import error
This appears AFTER successful training. Your model is already created! The error only affects optional TFLite conversion.

---

## 📚 Documentation

- **`WINDOWS_SETUP.md`** - Complete guide for Windows users
- **`TRAINING_SUCCESS.md`** - Training details and results
- **`requirements.txt`** - Full dependency list
- **`requirements-core.txt`** - Core dependencies only

---

## 🔧 Technical Details

### Applied Fixes:
1. ✅ Float division for input shape calculation
2. ✅ Dtype conversion (float64 → float32)
3. ✅ Multiprocessing disabled (prevents errors)
4. ✅ False positive validation handling
5. ✅ Auto total_length calculation
6. ✅ TFLite conversion error handling

### Key Technologies:
- **PyTorch 2.2.2** - Deep learning framework
- **OpenWakeWord 0.6.0** - Wake word detection
- **TensorFlow 2.20.0** - Model conversion
- **LibROSA** - Audio processing
- **ONNX** - Model export format

---

## 📈 Training Tips

### For Better Models:
1. **More data:** 100+ positive, 300+ negative samples
2. **Varied conditions:** Different speakers, backgrounds, volumes
3. **Longer training:** Increase `steps` to 1000-5000
4. **Quality audio:** Clear recordings, minimal noise

### Dataset Guidelines:
- **Positive samples:** Record your wake word multiple times
  - Different tones
  - Different speeds
  - Different distances from mic
- **Negative samples:** 
  - Background noise
  - Similar-sounding phrases
  - Common speech

---

## 🚢 Deployment

### Use Your Model:

**Python:**
```python
import onnxruntime as ort
session = ort.InferenceSession("models/hey_mel.onnx")
# Use session for inference
```

**Mobile (Convert to TFLite):**
```bash
# Use online conversion tools or:
pip install onnx-simplifier
onnx-simplifier models/hey_mel.onnx models/hey_mel_simplified.onnx
# Then convert to TFLite
```

---

## 📝 Platform-Specific Commands

| Task | macOS/Linux | Windows |
|------|-------------|---------|
| Activate venv | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| Train model | `./train.sh` | `train.bat` |
| Check dataset | `python check_dataset.py` | `python check_dataset.py` |
| View logs | `tail -f training.log` | `type training.log` |

---

## ✅ Quick Checklist

Before training:
- [ ] Python 3.12+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Audio files in dataset folders (5+ each)
- [ ] At least 4GB RAM free
- [ ] At least 2GB disk space free

---

## 🆘 Support

### Check Status:
```bash
python check_dataset.py
```

### Verify Environment:
```bash
python --version
pip list | grep torch
pip list | grep openwakeword
```

### Clean Reinstall:
```bash
# Backup your dataset first!
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
```

---

## 📦 Transfer to Another Machine

### Package Your Project:
```bash
# Exclude venv and large files
tar -czf train-tflite.tar.gz \
  --exclude='venv' \
  --exclude='models' \
  --exclude='*.log' \
  train-tflite/
```

### On New Machine:
```bash
# Extract
tar -xzf train-tflite.tar.gz
cd train-tflite

# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat
pip install -r requirements.txt

# Train
./train.sh  # or train.bat
```

---

## 🎓 Learning Resources

- **OpenWakeWord:** https://github.com/dscripka/openWakeWord
- **ONNX:** https://onnx.ai/
- **PyTorch:** https://pytorch.org/
- **Audio ML:** https://librosa.org/

---

## 📊 Project Stats

- **Scripts:** 8 Python files, 2 shell scripts, 2 batch files
- **Dependencies:** 120 packages
- **Model size:** ~618 KB (ONNX)
- **Training time:** 2-30 minutes
- **Platforms:** ✅ macOS, ✅ Windows, ✅ Linux

---

## 🎉 Success Criteria

Training is successful when you see:

```
Training: 100%|██████████| 500/500
==========================================
✓ Training Complete!
==========================================
Your model is ready:
  → models/hey_mel.onnx
```

---

**Version:** 1.0  
**Last Updated:** December 2, 2025  
**Status:** Production Ready ✅  
**Tested On:** macOS 14.6 (Apple Silicon), Windows 10/11

