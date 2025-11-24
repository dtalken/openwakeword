# OpenWakeWord TFLite Training Pipeline

Convert your WAV audio files into a TFLite wake word detection model for use in mobile apps (Flutter, React Native, etc.).

## 📁 Project Structure

```
train-tflite/
├── dataset/
│   ├── positive/          # Put your wake word samples here
│   │   ├── hey_mel_001.wav
│   │   ├── hey_mel_002.wav
│   │   └── ...
│   └── negative/          # Put background noise & other speech here
│       ├── noise_01.wav
│       ├── random_speech_001.wav
│       ├── tv_background.wav
│       └── silence.wav
├── models/                # Generated models will be saved here
├── normalize_audio.py     # Audio preprocessing script
├── train_config.yaml      # Training configuration
├── test_model.py         # Model testing script
├── check_dataset.py      # Dataset validation script
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install openwakeword torch torchaudio onnx onnxruntime pydub numpy
```

### Step 2: Prepare Your Dataset

1. **Collect positive samples** (your wake word):
   - Record 50-200 examples of your wake word
   - Use different speakers, accents, distances
   - Place in `dataset/positive/`

2. **Collect negative samples** (everything else):
   - Record 100-500 examples of:
     - Background noise (TV, music, traffic)
     - Other speech (not your wake word)
     - Silence or ambient sound
   - Place in `dataset/negative/`

**Audio Requirements:**
- Any format initially (WAV, MP3, etc.) - will be normalized
- Will be converted to: 16kHz, mono, PCM16

### Step 3: Validate Your Dataset

```bash
python check_dataset.py
```

This will show you:
- How many positive/negative samples you have
- If your dataset is ready for training
- Recommendations for improvement

### Step 4: Normalize Audio Files

Convert all audio to the required format (16kHz, mono, PCM16):

```bash
python normalize_audio.py
```

### Step 5: Configure Training

Edit `train_config.yaml` if needed:
- Change `wakeword_name` to your wake word (default: "hey_mel")
- Adjust `epochs`, `batch_size`, `learning_rate`
- Enable/disable augmentation options

### Step 6: Train the Model

```bash
python3 -m openwakeword.train --config train_config.yaml
```

Training will take several minutes to hours depending on:
- Dataset size
- Number of epochs
- Your hardware (GPU recommended)

**Output files** (in `models/` directory):
- `hey_mel.tflite` ← **This is what you need!**
- `hey_mel.onnx`
- `hey_mel.json`

### Step 7: Test Your Model

Test with a single audio file:

```bash
python test_model.py dataset/positive/hey_mel_001.wav
```

Or test directly with Python:

```bash
python3 -c "from openwakeword.model import Model; m = Model(wakeword_models=['models/hey_mel.tflite']); print('Model loaded successfully!')"
```

## 📱 Using in Flutter

### 1. Copy Model to Flutter Assets

```
your_flutter_app/
└── assets/
    └── models/
        ├── hey_mel.tflite
        └── labels.txt
```

Create `labels.txt`:
```
hey_mel
background
```

### 2. Update pubspec.yaml

```yaml
flutter:
  assets:
    - assets/models/hey_mel.tflite
    - assets/models/labels.txt
```

### 3. Add Dependencies

```yaml
dependencies:
  tflite_flutter: ^0.10.4
```

### 4. Load Model in Dart

```dart
import 'package:tflite_flutter/tflite_flutter.dart';
import 'dart:typed_data';

late Interpreter _interpreter;

Future<void> loadModel() async {
  _interpreter = await Interpreter.fromAsset(
    'models/hey_mel.tflite',
    options: InterpreterOptions()..threads = 2,
  );
  print("Wake word model loaded.");
}

// Use with your PCM16 audio stream
Future<double> detectWakeWord(Float32List audioData) async {
  var output = List.filled(1, 0.0).reshape([1, 1]);
  _interpreter.run(audioData, output);
  return output[0][0];  // Returns confidence score (0.0 to 1.0)
}
```

## 🎯 Tips for Better Accuracy

### Dataset Quality
- **More data = better model**
  - Positive: 50-200 samples minimum
  - Negative: 100-500 samples minimum
  
- **Diversity matters**
  - Multiple speakers
  - Different accents
  - Various background noise levels
  - Different recording distances

### Negative Samples Sources
- Record ambient noise from target environment
- TV/radio speech
- Music
- Other common phrases
- Silence (important!)
- Public datasets: Common Voice, LibriSpeech

### Training Tips
- Start with 40 epochs, adjust if needed
- Use data augmentation (enabled by default)
- Monitor training loss
- Test with real-world audio

### Flutter Integration Tips
- Use smoothing (average last 3-5 predictions)
- Set appropriate threshold (typically 0.5-0.8)
- Implement cooldown period after detection
- Test extensively in target environment

## 🛠️ Troubleshooting

### "Model performs poorly"
- Add more diverse training data
- Increase epochs (try 60-80)
- Check that audio is properly normalized
- Add more negative samples

### "Too many false positives"
- Add more negative samples
- Increase detection threshold in app
- Add smoothing/averaging

### "Misses real wake words"
- Add more positive samples with variations
- Lower detection threshold
- Check audio input quality

### "Training fails"
- Ensure dataset structure is correct
- Check that all WAV files are valid
- Verify Python dependencies installed
- Check GPU/memory availability

## 📚 Additional Resources

- [OpenWakeWord Documentation](https://github.com/dscripka/openWakeWord)
- [TFLite Flutter Plugin](https://pub.dev/packages/tflite_flutter)
- [Common Voice Dataset](https://commonvoice.mozilla.org/) (for negative samples)

## 🔄 Workflow Summary

```
1. Collect WAV files → dataset/positive/ and dataset/negative/
2. python check_dataset.py (validate)
3. python normalize_audio.py (preprocess)
4. openwakeword-train --config train_config.yaml (train)
5. python test_model.py <test.wav> (test)
6. Copy models/hey_mel.tflite to Flutter app
7. Deploy! 🚀
```

## 📝 License

This project uses OpenWakeWord. Check their repository for licensing terms.

---

**Need help?** Check the troubleshooting section or open an issue with details about your dataset and error messages.

