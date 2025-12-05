# Windows Setup - Super Simple Guide

## For New Windows Machine (Simplest Method)

### Option 1: One-Command Setup (Recommended) ⭐

**On current machine:**
```bash
create_package.bat
```

This creates an `OpenWakeWord_Package` folder.

**Copy to new machine:**
- Copy the entire `OpenWakeWord_Package` folder to new Windows machine
- That's it!

**On new machine:**
```bash
cd OpenWakeWord_Package
setup_windows.bat
```

Wait 5-10 minutes. Done!

---

### Option 2: Manual File Transfer

**Copy these 13 files** to new machine:

1. `setup_windows.bat` ⭐ (MAIN INSTALLER)
2. `requirements-windows-fixed.txt`
3. `patch_speechbrain.py`
4. `fix_torchaudio_backend.py`
5. `fix_trim_mmap.py`
6. `apply_fixes.py`
7. `train.bat`
8. `train_config.yaml`
9. `check_dataset.py`
10. `normalize_audio.py`
11. `prepare_data.py`
12. `final_onnx_to_tflite.py`
13. `test_model.py`

**On new machine:**
```bash
setup_windows.bat
```

---

## What You Need on New Machine

- ✅ Python 3.13 (from python.org)
- ✅ Internet connection (downloads models)
- ✅ 1GB free disk space
- ❌ NO Visual Studio needed
- ❌ NO FFmpeg needed
- ❌ NO manual configuration needed

---

## After Setup - How to Train

### 1. Add Audio Files
```
dataset/
├── positive/  ← Put "Hey Mel" recordings here (WAV files)
└── negative/  ← Put background noise/other speech here (WAV files)
```

**Minimum**: 20 positive + 40 negative  
**Recommended**: 50 positive + 100 negative

### 2. Train Model
```bash
train.bat
```

Takes 5-10 minutes. Output:
```
>>> Training SUCCEEDED! <<<

Your models are ready:
  >> models\hey_mel.onnx
  >> models\hey_mel.tflite
```

### 3. Test Model
```bash
python test_model.py dataset\positive\sample.wav
```

---

## Key Fixes Included

All these issues are automatically fixed by `setup_windows.bat`:

✅ Torchaudio version (uses 2.6.0, no FFmpeg needed)  
✅ SpeechBrain compatibility  
✅ Windows file locking  
✅ Missing dependencies  
✅ Resource downloads  
✅ Training patches  

---

## Comparison: Before vs After

### Before (Complex):
1. Install Python
2. Install dependencies
3. Get errors
4. Search for solutions
5. Apply manual patches
6. Try again
7. More errors...
8. Eventually works

### After (Simple):
1. Copy files
2. Run `setup_windows.bat`
3. Run `train.bat`
4. Done!

---

## File Sizes

Total package size: ~100KB (scripts only)

After setup (with dependencies): ~2-3GB

Models created: ~1.2MB (both ONNX + TFLite)

---

## Support Files Created

- `QUICK_START_NEW_MACHINE.txt` - Quick reference
- `SETUP_NEW_MACHINE.md` - Detailed guide
- `FINAL_STATUS.md` - Current machine status
- `requirements-windows-fixed.txt` - Tested dependency versions

---

## Questions?

**Q: Do I need Visual Studio or C++ compilers?**  
A: No! All packages have pre-built wheels for Windows.

**Q: Do I need FFmpeg?**  
A: No! We use torchaudio 2.6.0 which doesn't require it.

**Q: Will this work on Python 3.11 or 3.12?**  
A: Yes, but Python 3.13 is recommended and tested.

**Q: Can I use this on Linux/Mac?**  
A: No, this is Windows-specific. Linux/Mac have different setup.

**Q: How long does training take?**  
A: 5-10 minutes for small datasets (10-20 samples)
   10-30 minutes for medium datasets (50-100 samples)
   30-60 minutes for large datasets (200-500 samples)

---

## Success! 🎉

Your new machine will be training-ready in under 10 minutes!

