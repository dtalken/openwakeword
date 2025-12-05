#!/usr/bin/env python3
"""
Download missing OpenWakeWord resource files.
The mel spectrogram model is required for training.
"""
import os
import urllib.request

def download_resources():
    """Download missing OpenWakeWord resource files"""
    try:
        import openwakeword
        opw_dir = os.path.dirname(openwakeword.__file__)
        
        # Create resources/models directory
        models_dir = os.path.join(opw_dir, 'resources', 'models')
        os.makedirs(models_dir, exist_ok=True)
        
        # URL for the melspectrogram model (from OpenWakeWord GitHub)
        melspec_url = "https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/melspectrogram.onnx"
        embedding_url = "https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/embedding_model.onnx"
        
        melspec_file = os.path.join(models_dir, "melspectrogram.onnx")
        embedding_file = os.path.join(models_dir, "embedding_model.onnx")
        
        print("Downloading OpenWakeWord resource files...")
        print("=" * 60)
        
        # Download melspectrogram model
        if not os.path.exists(melspec_file):
            print(f"Downloading melspectrogram.onnx...")
            urllib.request.urlretrieve(melspec_url, melspec_file)
            print(f"✓ Downloaded: {melspec_file}")
        else:
            print(f"✓ Already exists: {melspec_file}")
        
        # Download embedding model
        if not os.path.exists(embedding_file):
            print(f"Downloading embedding_model.onnx...")
            urllib.request.urlretrieve(embedding_url, embedding_file)
            print(f"✓ Downloaded: {embedding_file}")
        else:
            print(f"✓ Already exists: {embedding_file}")
        
        print("=" * 60)
        print("✅ Resource files are ready!")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading resources: {e}")
        return False

if __name__ == '__main__':
    success = download_resources()
    if not success:
        print("\n❌ Failed to download resources")
        print("You may need to manually download from:")
        print("https://github.com/dscripka/openWakeWord/tree/main/openwakeword/resources/models")

