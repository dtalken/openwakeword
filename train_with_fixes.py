#!/usr/bin/env python3
"""
Training wrapper that applies all necessary compatibility fixes before training.
This ensures torchaudio compatibility with SpeechBrain is patched before any imports.
"""
import sys
import os

# CRITICAL: Patch torchaudio BEFORE any other imports
# This must happen before speechbrain is imported (which happens via openwakeword)
try:
    import fix_torchaudio_compat
except ImportError:
    # Fallback: patch directly if fix_torchaudio_compat is not available
    try:
        import torchaudio
        if not hasattr(torchaudio, 'list_audio_backends'):
            def list_audio_backends():
                """List available audio backends"""
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
            print("✓ Patched torchaudio: added list_audio_backends()")
    except ImportError:
        pass

# Now apply other fixes
try:
    import apply_fixes
    apply_fixes.apply_fixes()
except Exception as e:
    print(f"⚠️  Warning: Could not apply all fixes: {e}")
    print("Continuing with training anyway...")

# Now run the training command
if __name__ == '__main__':
    import subprocess
    
    # Get command line arguments (skip script name)
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Default arguments if none provided
    if not args:
        args = ['--training_config', 'train_config.yaml', '--augment_clips', '--overwrite', '--train_model']
    
    # Run the training module using subprocess
    # This ensures the torchaudio fix is already applied before the module imports
    cmd = [sys.executable, '-m', 'openwakeword.train'] + args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)

