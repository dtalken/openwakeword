#!/usr/bin/env python3
"""
Prepare data structure for OpenWakeWord training when using pre-recorded audio
"""
import os
import shutil
from pathlib import Path

def prepare_data():
    """Split dataset into train/test directories as expected by OpenWakeWord"""
    
    # Create output directories
    model_dir = Path("models/hey_mel")
    positive_train = model_dir / "positive_train"
    positive_test = model_dir / "positive_test"
    negative_train = model_dir / "negative_train"
    negative_test = model_dir / "negative_test"
    
    for dir_path in [positive_train, positive_test, negative_train, negative_test]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Split positive samples (80/20 train/test)
    positive_files = list(Path("dataset/positive").glob("*.wav"))
    n_test = max(1, len(positive_files) // 5)  # 20% for test, min 1
    
    for i, file in enumerate(positive_files):
        if i < n_test:
            shutil.copy2(file, positive_test / file.name)
        else:
            shutil.copy2(file, positive_train / file.name)
    
    # Split negative samples (80/20 train/test)
    negative_files = list(Path("dataset/negative").glob("*.wav"))
    n_test = max(1, len(negative_files) // 5)  # 20% for test, min 1
    
    for i, file in enumerate(negative_files):
        if i < n_test:
            shutil.copy2(file, negative_test / file.name)
        else:
            shutil.copy2(file, negative_train / file.name)
    
    print(f"[OK] Data prepared:")
    print(f"  Positive train: {len(list(positive_train.glob('*.wav')))} files")
    print(f"  Positive test:  {len(list(positive_test.glob('*.wav')))} files")
    print(f"  Negative train: {len(list(negative_train.glob('*.wav')))} files")
    print(f"  Negative test:  {len(list(negative_test.glob('*.wav')))} files")

if __name__ == '__main__':
    prepare_data()


