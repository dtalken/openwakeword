#!/usr/bin/env python3
"""
Apply all necessary fixes to openwakeword train.py for small datasets
"""
import os
import shutil

# Apply torchaudio compatibility fix before any other imports
try:
    import fix_torchaudio_compat
except ImportError:
    # If fix_torchaudio_compat.py is not in path, try to patch directly
    try:
        import torchaudio
        if not hasattr(torchaudio, 'list_audio_backends'):
            def list_audio_backends():
                backends = []
                try:
                    import soundfile
                    backends.append('soundfile')
                except ImportError:
                    pass
                try:
                    import soxr
                    backends.append('sox')
                except ImportError:
                    pass
                return backends
            torchaudio.list_audio_backends = list_audio_backends
    except ImportError:
        pass

def apply_fixes():
    """Apply critical fixes to the openwakeword training code"""
    
    try:
        import openwakeword.train as train_module
    except ImportError as e:
        print(f"[WARN]  Warning: Could not import openwakeword.train: {e}")
        print("This is likely due to missing dependencies. Training fixes will be skipped.")
        print("Please install missing dependencies and try again.")
        return
    
    train_file = train_module.__file__
    backup_file = train_file + '.original_backup'
    
    # Backup if not already done
    if not os.path.exists(backup_file):
        shutil.copy2(train_file, backup_file)
        print(f"[OK] Backed up original to: {backup_file}")
    
    with open(train_file, 'r') as f:
        code = f.read()
    
    # Apply all fixes
    fixes_applied = []
    
    # Fix 1: Float division for total_length
    if 'config["total_length"]//16000' in code:
        code = code.replace(
            'config["total_length"]//16000',
            'config["total_length"]/16000'
        )
        fixes_applied.append("total_length division")
    
    # Fix 2: Dtype for validation data
    if 'X_val_pos = np.load(os.path.join(feature_save_dir, "positive_features_test.npy"))' in code:
        code = code.replace(
            'X_val_pos = np.load(os.path.join(feature_save_dir, "positive_features_test.npy"))',
            'X_val_pos = np.load(os.path.join(feature_save_dir, "positive_features_test.npy")).astype(np.float32)'
        )
        fixes_applied.append("positive validation dtype")
    
    if 'X_val_neg = np.load(os.path.join(feature_save_dir, "negative_features_test.npy"))' in code:
        code = code.replace(
            'X_val_neg = np.load(os.path.join(feature_save_dir, "negative_features_test.npy"))',
            'X_val_neg = np.load(os.path.join(feature_save_dir, "negative_features_test.npy")).astype(np.float32)'
        )
        fixes_applied.append("negative validation dtype")
    
    # Fix 3: Disable multiprocessing
    if 'num_workers=n_cpus, prefetch_factor=16' in code:
        code = code.replace(
            'num_workers=n_cpus, prefetch_factor=16',
            'num_workers=0'
        )
        fixes_applied.append("multiprocessing")
    
    # Fix 4: Handle missing false positive validation
    if 'X_val_fp = np.load(config["false_positive_validation_data_path"])' in code:
        code = code.replace(
            'X_val_fp = np.load(config["false_positive_validation_data_path"])',
            'X_val_fp = np.load(config["false_positive_validation_data_path"]) if config.get("false_positive_validation_data_path") else np.zeros((1, 1536), dtype=np.float32)'
        )
        fixes_applied.append("false positive validation")
    
    # Fix 5: Skip FP validation reshaping if None
    if 'X_val_fp = np.array([X_val_fp[i:i+input_shape[0]] for i in range(0, X_val_fp.shape[0]-input_shape[0], 1)])' in code:
        code = code.replace(
            'X_val_fp = np.array([X_val_fp[i:i+input_shape[0]] for i in range(0, X_val_fp.shape[0]-input_shape[0], 1)])',
            'X_val_fp = np.array([X_val_fp[i:i+input_shape[0]] for i in range(0, X_val_fp.shape[0]-input_shape[0], 1)]) if X_val_fp.shape[0] > input_shape[0] else X_val_fp[:1]'
        )
        fixes_applied.append("FP validation reshaping")
    
    # Fix 6: Handle auto total_length calculation  
    if 'for i in range(n):\n        sr, dat = scipy.io.wavfile.read(positive_clips[np.random.randint(0, len(positive_clips))])' in code:
        code = code.replace(
            'for i in range(n):\n        sr, dat = scipy.io.wavfile.read(positive_clips[np.random.randint(0, len(positive_clips))])',
            'for i in range(min(n, len(positive_clips)) if len(positive_clips) > 0 else 0):\n        sr, dat = scipy.io.wavfile.read(positive_clips[np.random.randint(0, len(positive_clips))])'
        )
        fixes_applied.append("auto total_length calculation")
    
    # Fix 7: Disable TFLite conversion (ONNX model is sufficient)
    if 'convert_onnx_to_tflite(' in code:
        # Simply comment out the conversion - ONNX works fine
        code = code.replace(
            'convert_onnx_to_tflite(os.path.join(config["output_dir"], config["model_name"] + ".onnx"),\n                       os.path.join(config["output_dir"], config["model_name"] + ".tflite"))',
            'pass  # TFLite conversion disabled - ONNX model is ready and working'
        )
        fixes_applied.append("TFLite conversion disabled (ONNX ready)")
    
    # Write patched version
    with open(train_file, 'w') as f:
        f.write(code)
    
    # Clear bytecode cache
    pycache = os.path.join(os.path.dirname(train_file), '__pycache__')
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
    
    print("=" * 60)
    print("[OK] Applied fixes:")
    for fix in fixes_applied:
        print(f"  - {fix}")
    print("=" * 60)
    print("\n[OK] Training code is now patched and ready!")
    print(f"[OK] Original backed up at: {backup_file}")
    
if __name__ == '__main__':
    apply_fixes()


