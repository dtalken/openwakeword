#!/usr/bin/env python3
"""
Check dataset structure and count audio files
"""

import os
from pathlib import Path

def check_dataset(root_dir="dataset"):
    """
    Verify dataset structure and count files
    """
    print("=" * 60)
    print("DATASET VALIDATION")
    print("=" * 60)
    
    positive_dir = os.path.join(root_dir, "positive")
    negative_dir = os.path.join(root_dir, "negative")
    
    # Check if directories exist
    if not os.path.exists(positive_dir):
        print(f"⚠ Warning: {positive_dir} does not exist!")
        positive_count = 0
    else:
        positive_files = [f for f in os.listdir(positive_dir) if f.lower().endswith('.wav')]
        positive_count = len(positive_files)
        print(f"\n[OK] Positive samples: {positive_count} files")
        if positive_count > 0:
            print(f"  Location: {positive_dir}")
            print(f"  Examples: {', '.join(positive_files[:3])}")
    
    if not os.path.exists(negative_dir):
        print(f"\n⚠ Warning: {negative_dir} does not exist!")
        negative_count = 0
    else:
        negative_files = [f for f in os.listdir(negative_dir) if f.lower().endswith('.wav')]
        negative_count = len(negative_files)
        print(f"\n[OK] Negative samples: {negative_count} files")
        if negative_count > 0:
            print(f"  Location: {negative_dir}")
            print(f"  Examples: {', '.join(negative_files[:3])}")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total positive: {positive_count}")
    print(f"Total negative: {negative_count}")
    print(f"Total dataset:  {positive_count + negative_count}")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if positive_count < 50:
        print("⚠ Consider adding more positive samples (recommended: 50-200)")
    else:
        print("[OK] Positive sample count looks good")
    
    if negative_count < 100:
        print("⚠ Consider adding more negative samples (recommended: 100-500)")
    else:
        print("[OK] Negative sample count looks good")
    
    if positive_count == 0 or negative_count == 0:
        print("\n[ERROR] Dataset is incomplete! You need both positive and negative samples.")
        print("\nNext steps:")
        print("1. Add your wake word WAV files to: dataset/positive/")
        print("2. Add background noise/other speech to: dataset/negative/")
        print("3. Run: python normalize_audio.py")
        print("4. Run this script again to verify")
    else:
        print("\n[OK] Dataset is ready for training!")
        print("\nNext steps:")
        print("1. Run: python normalize_audio.py")
        print("2. Run: openwakeword-train --config train_config.yaml")

if __name__ == "__main__":
    check_dataset()


