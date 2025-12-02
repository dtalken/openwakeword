# ⚡ Quick Start Guide

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your WAV files
#    - Positive samples → dataset/positive/
#    - Negative samples → dataset/negative/

# 3. Run training (automated)
bash train.sh

# 4. Your TFLite model will be in models/hey_mel.tflite
```

## Step-by-Step Instructions

### 1️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Prepare Your Audio Files

**Positive Samples** (your wake word):
- Record yourself saying the wake word 50-200 times
- Get different people to say it
- Vary the distance, volume, accent
- Save as: `dataset/positive/*.wav`

Example files:
```
dataset/positive/hey_mel_001.wav
dataset/positive/hey_mel_002.wav
dataset/positive/hey_mel_003.wav
...
```

**Negative Samples** (background noise + other speech):
- Record 100-500 samples of:
  - TV/radio in background
  - Music
  - Random conversation
  - Ambient noise
  - Silence
- Save as: `dataset/negative/*.wav`

Example files:
```
dataset/negative/noise_01.wav
dataset/negative/tv_background.wav
dataset/negative/random_speech_001.wav
dataset/negative/silence.wav
...
```

### 3️⃣ Verify Dataset

```bash
python check_dataset.py
```

Should show:
- ✓ Positive samples: XX files
- ✓ Negative samples: XX files
- ✓ Dataset is ready for training!

### 4️⃣ Train the Model

**Option A: Automated (Recommended)**
```bash
bash train.sh
```

**Option B: Manual Steps**
```bash
# Normalize audio
python3 normalize_audio.py

# Train
python3 -m openwakeword.train --config train_config.yaml
```

### 5️⃣ Test Your Model

```bash
python test_model.py dataset/positive/hey_mel_001.wav
```

### 6️⃣ Deploy to Flutter

Copy the generated file:
```
models/hey_mel.tflite → your_flutter_app/assets/models/
```

See `README.md` for Flutter integration code.

## 📊 Expected Dataset Sizes

| Quality | Positive Samples | Negative Samples | Training Time |
|---------|-----------------|------------------|---------------|
| Minimum | 50              | 100              | 5-10 min      |
| Good    | 100             | 200              | 10-20 min     |
| Excellent | 200+          | 500+             | 30-60 min     |

## 🎯 Common Issues

**"Not enough samples"**
- Add more WAV files to dataset folders

**"Training takes too long"**
- Reduce epochs in `train_config.yaml` (try 20)
- Use a machine with GPU

**"Model not accurate"**
- Add more diverse samples
- Increase epochs to 60-80
- Add more negative samples

## 🔗 What's Next?

1. ✅ Train model → Get `models/hey_mel.tflite`
2. 📱 Integrate into Flutter app
3. 🧪 Test in real environment
4. 🔄 Iterate: collect more data → retrain

---

**Full documentation:** See `README.md`

