#!/usr/bin/env python3
"""
Audio Normalization Script for OpenWakeWord Training
Normalizes all WAV files to 16kHz, mono, PCM16 format
"""

import os

try:
    # Preferred path: use pydub if it works in this Python version
    from pydub import AudioSegment  # type: ignore
    _USE_PYDUB = True
except Exception:
    # Fallback: use librosa + soundfile (avoids audioop/pyaudioop issues on 3.13)
    AudioSegment = None  # type: ignore
    _USE_PYDUB = False
    import librosa
    import soundfile as sf

def normalize_audio_files(root_dir="dataset"):
    """
    Recursively normalize all WAV files in the dataset directory
    to 16kHz, mono, PCM16 format (required for TFLite training)
    """
    processed_count = 0
    error_count = 0
    
    print(f"Starting audio normalization in: {root_dir}")
    print("-" * 60)
    
    for folder, subfolders, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith(".wav"):
                path = os.path.join(folder, f)
                try:
                    if _USE_PYDUB and AudioSegment is not None:
                        # Load audio file with pydub
                        audio = AudioSegment.from_file(path)
                        # Normalize to 16kHz, mono, 16-bit PCM
                        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                        # Export back to the same file
                        audio.export(path, format="wav")
                    else:
                        # Librosa + soundfile path (no audioop dependency)
                        y, sr = librosa.load(path, sr=16000, mono=True)
                        # Write as 16‑bit PCM WAV
                        sf.write(path, y, 16000, subtype="PCM_16")
                    
                    processed_count += 1
                    print(f"[OK] Normalized: {path}")
                    
                except Exception as e:
                    error_count += 1
                    print(f"✗ Error processing {path}: {str(e)}")
    
    print("-" * 60)
    print(f"\nNormalization complete!")
    print(f"  Successfully processed: {processed_count} files")
    if error_count > 0:
        print(f"  Errors encountered: {error_count} files")
    print(f"\nAll WAV files are now 16kHz mono PCM16 format.")

if __name__ == "__main__":
    normalize_audio_files()


