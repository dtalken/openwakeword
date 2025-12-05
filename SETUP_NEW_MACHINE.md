# 🚀 Simple Setup for New Windows Machine

## One-Command Installation

Download these files to your new machine and run:

```bash
setup_windows.bat
```

That's it! Everything will be installed and configured automatically.

## What setup_windows.bat Does

1. Upgrades pip
2. Installs correct versions of all dependencies
3. Downloads OpenWakeWord resources
4. Applies all compatibility patches automatically
5. Verifies installation

**Time**: 5-10 minutes

## Files Needed on New Machine

**Required Files** (copy these):
```
setup_windows.bat                    ← Main setup script
requirements-windows-fixed.txt       ← Dependency list
patch_speechbrain.py                 ← Compatibility fix
fix_torchaudio_backend.py            ← Backend fix
fix_trim_mmap.py                     ← Windows file locking fix
apply_fixes.py                       ← Training patches
train.bat                            ← Training script
train_config.yaml                    ← Training configuration
check_dataset.py                     ← Dataset validator
normalize_audio.py                   ← Audio normalizer
prepare_data.py                      ← Data preparation
final_onnx_to_tflite.py              ← TFLite converter
test_model.py                        ← Model tester
```

## Alternative: Manual Installation

If you prefer manual steps:

### Step 1: Install Python 3.13
Download from python.org

### Step 2: Install Dependencies
```bash
pip install -r requirements-windows-fixed.txt
```

### Step 3: Download Resources
```bash
python -c "from openwakeword.utils import download_models; download_models()"
```

### Step 4: Apply Patches
```bash
python patch_speechbrain.py
python fix_torchaudio_backend.py
python fix_trim_mmap.py
python apply_fixes.py
```

### Step 5: Verify
```bash
python -c "from openwakeword import train; print('OK')"
```

## After Setup

### Add Your Audio Data
```
dataset/
├── positive/  ← Your "Hey Mel" recordings (WAV files)
└── negative/  ← Background noise, other speech (WAV files)
```

### Train
```bash
train.bat
```

### Test
```bash
python test_model.py dataset\positive\sample.wav
```

## Key Version Requirements

**Critical versions** (don't change these):
- `torch==2.6.0` (newer versions need FFmpeg)
- `torchaudio==2.6.0` (newer versions need FFmpeg)

Other packages can use latest versions.

## What Gets Fixed Automatically

✅ Torchaudio compatibility with SpeechBrain  
✅ Windows file locking issues  
✅ Missing resource files  
✅ Training code patches for small datasets  
✅ All import errors  

## Time to Train

With the setup complete:
- Setup time: 5-10 minutes (one time)
- Training time: 5-10 minutes per session
- Total: ~15 minutes from scratch to trained model

## Troubleshooting

If setup fails:
1. Make sure Python 3.13 is installed
2. Run as Administrator if needed
3. Check internet connection (downloads resources)

## Success Indicator

After running `train.bat`, you should see:

```
>>> Training SUCCEEDED! <<<

Your models are ready:
  >> models\hey_mel.onnx
  >> models\hey_mel.tflite
```

No error messages, clean output!

