#!/usr/bin/env python3
"""
Audio Normalization Script for OpenWakeWord Training
Normalizes all WAV files to 16kHz, mono, PCM16 format
"""

import os
from pydub import AudioSegment

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
                    # Load audio file
                    audio = AudioSegment.from_file(path)
                    
                    # Normalize to 16kHz, mono, 16-bit PCM
                    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                    
                    # Export back to the same file
                    audio.export(path, format="wav")
                    
                    processed_count += 1
                    print(f"✓ Normalized: {path}")
                    
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

