# 🎯 Complete Workflow: WAV → TFLite

## Visual Pipeline

```
┌─────────────────┐
│  Collect WAVs   │  You record/collect audio samples
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Organize Data  │  dataset/positive/ & dataset/negative/
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validate       │  python check_dataset.py
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Normalize      │  python normalize_audio.py → 16kHz mono PCM16
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Train Model    │  openwakeword-train → TFLite + ONNX + JSON
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Test Model     │  python test_model.py <file.wav>
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deploy         │  Copy .tflite to Flutter/mobile app
└─────────────────┘
```

## Detailed Steps

### Phase 1: Data Collection

**Goal:** Gather audio samples for training

**Positive Samples** (50-200 files):
- Your wake word spoken multiple times
- Different speakers
- Different environments
- Different volumes/distances
- Save to: `dataset/positive/`

**Negative Samples** (100-500 files):
- Background noise
- Other speech (not the wake word)
- Music, TV, radio
- Silence/ambient sound
- Save to: `dataset/negative/`

**File naming examples:**
```
dataset/positive/hey_mel_001.wav
dataset/positive/hey_mel_002.wav
dataset/positive/hey_mel_speaker2_001.wav

dataset/negative/ambient_noise_001.wav
dataset/negative/tv_background.wav
dataset/negative/random_speech_001.wav
dataset/negative/silence.wav
```

---

### Phase 2: Validation

**Command:**
```bash
python check_dataset.py
```

**What it does:**
- Counts positive/negative samples
- Checks folder structure
- Provides recommendations
- Confirms readiness for training

**Expected output:**
```
✓ Positive samples: 120 files
✓ Negative samples: 300 files
✓ Dataset is ready for training!
```

---

### Phase 3: Preprocessing

**Command:**
```bash
python normalize_audio.py
```

**What it does:**
- Converts all audio to 16kHz sample rate
- Converts to mono (1 channel)
- Converts to PCM16 format
- Overwrites original files with normalized versions

**Why needed:**
- TFLite models require consistent audio format
- 16kHz is optimal for speech recognition
- Mono reduces model complexity
- PCM16 is standard uncompressed format

---

### Phase 4: Training

**Command:**
```bash
python3 -m openwakeword.train --config train_config.yaml
```

**What it does:**
- Loads audio from dataset folders
- Applies data augmentation (noise, pitch shift, etc.)
- Trains neural network model
- Generates multiple output formats

**Configuration** (train_config.yaml):
```yaml
dataset_dir: dataset
wakeword_name: hey_mel        # Change this!
sample_rate: 16000
epochs: 40                     # More = better (slower)
batch_size: 32
learning_rate: 0.001
augmentation:
  noise: true
  pitch_shift: true
  time_stretch: true
  random_gain: true
```

**Output files** (in `models/` directory):
- `hey_mel.tflite` ← **Primary output for mobile**
- `hey_mel.onnx` ← For server/desktop use
- `hey_mel.json` ← Metadata

**Training time:**
- Small dataset (50+100): 5-10 minutes
- Medium dataset (100+200): 10-20 minutes
- Large dataset (200+500): 30-60 minutes
- GPU accelerates training significantly

---

### Phase 5: Testing

**Command:**
```bash
python test_model.py dataset/positive/hey_mel_001.wav
```

**What it does:**
- Loads the trained TFLite model
- Runs inference on test audio
- Shows detection confidence score

**Manual testing:**
```bash
# Test with positive sample (should detect)
python test_model.py dataset/positive/hey_mel_050.wav

# Test with negative sample (should NOT detect)
python test_model.py dataset/negative/noise_01.wav
```

**Good results:**
- Positive samples: confidence > 0.7
- Negative samples: confidence < 0.3

---

### Phase 6: Deployment

**For Flutter:**

1. **Copy model file:**
   ```
   cp models/hey_mel.tflite your_flutter_app/assets/models/
   ```

2. **Create labels file:**
   ```
   echo "hey_mel\nbackground" > your_flutter_app/assets/models/labels.txt
   ```

3. **Update pubspec.yaml:**
   ```yaml
   flutter:
     assets:
       - assets/models/hey_mel.tflite
       - assets/models/labels.txt
   
   dependencies:
     tflite_flutter: ^0.10.4
   ```

4. **Load in Dart:**
   ```dart
   import 'package:tflite_flutter/tflite_flutter.dart';
   
   late Interpreter _interpreter;
   
   Future<void> loadModel() async {
     _interpreter = await Interpreter.fromAsset(
       'models/hey_mel.tflite',
       options: InterpreterOptions()..threads = 2,
     );
   }
   
   Future<double> detect(Float32List audioData) async {
     var output = List.filled(1, 0.0).reshape([1, 1]);
     _interpreter.run(audioData, output);
     return output[0][0];  // 0.0 to 1.0
   }
   ```

---

## File Requirements Summary

### Input (What You Provide)
- **Audio files**: WAV, MP3, or any format
- **Quantity**: 
  - Minimum: 50 positive + 100 negative
  - Recommended: 100 positive + 200 negative
  - Optimal: 200+ positive + 500+ negative

### Processing (Automatic)
- **Normalized to**: 16kHz, mono, PCM16 WAV
- **Augmentation**: Noise, pitch, stretch, gain

### Output (What You Get)
- **TFLite model**: `models/hey_mel.tflite` (500KB - 2MB)
- **Ready for**: Flutter, React Native, TensorFlow Lite

---

## Command Cheat Sheet

```bash
# Setup (recommended for Apple Silicon)
bash setup_environment.sh

# Or manual setup
pip3 install -r requirements.txt

# Validate
python3 check_dataset.py

# Preprocess
python3 normalize_audio.py

# Train (option 1: automated)
bash train.sh

# Train (option 2: manual)
python3 -m openwakeword.train --config train_config.yaml

# Test
python3 test_model.py <audio_file.wav>

# Check file structure
ls -R dataset/
ls -lh models/
```

---

## Success Checklist

- [ ] Installed Python dependencies
- [ ] Created dataset/positive/ folder
- [ ] Created dataset/negative/ folder
- [ ] Added 50+ positive WAV files
- [ ] Added 100+ negative WAV files
- [ ] Ran check_dataset.py successfully
- [ ] Ran normalize_audio.py
- [ ] Edited train_config.yaml (changed wakeword_name)
- [ ] Ran training command
- [ ] Got models/hey_mel.tflite output
- [ ] Tested model with test_model.py
- [ ] Copied .tflite to Flutter app
- [ ] Model works in production!

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Dataset not found" | Create dataset/positive and dataset/negative folders |
| "No WAV files" | Add .wav files to dataset folders |
| "Training fails" | Check that files are valid audio, run normalize first |
| "Model inaccurate" | Add more diverse samples, increase epochs |
| "Too slow" | Reduce epochs, use GPU, reduce dataset size |
| "False positives" | Add more negative samples, adjust threshold in app |
| "Misses wake word" | Add more positive samples with variations |

---

**Ready to start?** Follow `QUICKSTART.md` for the fastest path to your first model!

