# 🚀 Start Here: WAV to TFLite Pipeline

Welcome! This project converts your WAV audio files into a TFLite wake word detection model.

## 📦 What's Included

```
train-tflite/
├── 📄 START_HERE.md          ← You are here!
├── 📄 QUICKSTART.md          ← Fast track (5 commands)
├── 📄 README.md              ← Full documentation
├── 📄 WORKFLOW.md            ← Detailed pipeline explanation
│
├── 🐍 Python Scripts:
│   ├── normalize_audio.py    ← Converts audio to required format
│   ├── check_dataset.py      ← Validates your dataset
│   ├── test_model.py         ← Tests trained model
│   └── train.sh              ← Automated training script
│
├── ⚙️  Configuration:
│   ├── train_config.yaml     ← Training parameters
│   ├── requirements.txt      ← Python dependencies
│   └── .gitignore           ← Git ignore rules
│
└── 📁 Folders:
    ├── dataset/
    │   ├── positive/         ← Put wake word samples here
    │   └── negative/         ← Put noise/other speech here
    └── models/               ← Trained models appear here
```

## ⚡ 3-Minute Quick Start

### 1. Install Dependencies (30 seconds)

**🚨 IMPORTANT for Apple Silicon (M1/M2/M3) Macs:**

If you're getting architecture errors, run this:
```bash
bash fix_architecture.sh
```

This creates a clean virtual environment and fixes all architecture conflicts.

**Alternative options:**
```bash
# Option A: Automated setup
bash setup_environment.sh

# Option B: Manual install (may cause architecture issues)
pip3 install -r requirements.txt
```

**Note:** Virtual environment is **strongly recommended** to avoid architecture conflicts.

### 2. Add Your Audio Files (you do this)
- **Positive samples** (your wake word): → `dataset/positive/`
  - Example: hey_mel_001.wav, hey_mel_002.wav, etc.
  - Need: 50-200 files

- **Negative samples** (noise, other speech): → `dataset/negative/`
  - Example: noise_01.wav, tv_background.wav, etc.
  - Need: 100-500 files

### 3. Train Your Model (2 minutes)
```bash
bash train.sh
```

### 4. Get Your TFLite File
```bash
ls models/hey_mel.tflite
```

**That's it!** Your TFLite model is ready for Flutter/mobile deployment.

---

## 📚 Choose Your Path

### 🏃 I want to start immediately
→ Read **QUICKSTART.md**
- Minimal explanation
- Copy-paste commands
- Get model in 5 minutes

### 📖 I want full documentation
→ Read **README.md**
- Complete guide
- Troubleshooting
- Flutter integration
- Tips for accuracy

### 🔍 I want to understand the workflow
→ Read **WORKFLOW.md**
- Visual pipeline diagram
- Detailed step explanations
- File format requirements
- Technical details

---

## ✅ Pre-Flight Checklist

Before training, make sure you have:

- [ ] Python 3.8+ installed
- [ ] 50+ WAV files of your wake word
- [ ] 100+ WAV files of background noise/other speech
- [ ] 10-60 minutes for training (depending on dataset size)
- [ ] (Optional) GPU for faster training

---

## 🎯 Expected Results

After training, you'll get:

| File | Size | Purpose |
|------|------|---------|
| `hey_mel.tflite` | ~500KB-2MB | 🎯 Use this in Flutter |
| `hey_mel.onnx` | ~500KB-2MB | For server/desktop apps |
| `hey_mel.json` | ~1KB | Model metadata |

---

## 🆘 Need Help?

### Common Issues

**"I don't have negative samples"**
- Record ambient noise from your environment
- Use TV/radio in background
- Download from Common Voice dataset
- Record 30 seconds of silence

**"Where do I get WAV files?"**
- Record on your phone (use Voice Memos app)
- Ask friends/family to record
- Convert from MP3/M4A: `ffmpeg -i input.mp3 output.wav`
- Use text-to-speech services

**"Training failed"**
- Run: `python check_dataset.py` to diagnose
- Ensure WAV files are valid
- Run: `python normalize_audio.py` first
- Check error messages in terminal

**"Model not accurate"**
- Add more training data (especially negatives)
- Increase epochs to 60-80 in `train_config.yaml`
- Ensure diverse samples (different speakers, environments)

---

## 🔄 The Process (High-Level)

```
Your WAV Files
      ↓
Normalize to 16kHz mono
      ↓
Train Neural Network
      ↓
Generate TFLite Model
      ↓
Deploy to Flutter App
      ↓
Wake Word Detection! ✨
```

---

## 📞 Support

1. **Check documentation**: README.md has troubleshooting section
2. **Validate dataset**: Run `python check_dataset.py`
3. **Test model**: Run `python test_model.py <audio.wav>`
4. **OpenWakeWord issues**: https://github.com/dscripka/openWakeWord

---

## 🎓 Learning Path

```
Beginner     → QUICKSTART.md (just get it working)
              ↓
Intermediate → README.md (understand options)
              ↓
Advanced     → WORKFLOW.md (deep dive into pipeline)
              ↓
Expert       → Modify train_config.yaml & scripts
```

---

## 🚦 Ready to Start?

### Absolute Beginner Path:
```bash
# 1. Setup environment (fixes Apple Silicon issues)
bash setup_environment.sh

# 2. Add your WAV files to:
#    - dataset/positive/
#    - dataset/negative/

# 3. Train
bash train.sh

# Done! Your model is in models/hey_mel.tflite
```

### I Know What I'm Doing Path:
```bash
pip3 install -r requirements.txt
python3 check_dataset.py
python3 normalize_audio.py
python3 -m openwakeword.train --config train_config.yaml
python3 test_model.py test.wav
```

---

**Questions?** All answers are in **README.md**

**Let's build something awesome! 🚀**

