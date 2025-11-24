#!/usr/bin/env python3
"""
Test the trained TFLite model with audio files
"""

import sys
import os
import numpy as np

def test_model(model_path, audio_path):
    """
    Test the TFLite model with a given audio file
    """
    if not os.path.exists(model_path):
        print(f"❌ Error: Model file not found: {model_path}")
        print(f"\nMake sure you've trained the model first:")
        print(f"  bash train.sh")
        sys.exit(1)
    
    if not os.path.exists(audio_path):
        print(f"❌ Error: Audio file not found: {audio_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("TESTING MODEL")
    print("=" * 60)
    print(f"Model: {model_path}")
    print(f"Audio: {audio_path}")
    print("-" * 60)
    
    try:
        # Import OpenWakeWord
        from openwakeword.model import Model
        
        # Load the model
        print("Loading model...")
        model = Model(wakeword_models=[model_path])
        
        # Load and process audio
        print("Processing audio...")
        from pydub import AudioSegment
        
        audio = AudioSegment.from_file(audio_path)
        # Convert to 16kHz mono if needed
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
        
        # Run prediction
        print("Running inference...")
        prediction = model.predict(samples)
        
        # Get model name (filename without extension)
        model_name = os.path.basename(model_path).replace('.tflite', '')
        
        if model_name in prediction:
            score = prediction[model_name]
            print("\n" + "=" * 60)
            print("RESULT")
            print("=" * 60)
            print(f"Wake word: {model_name}")
            print(f"Confidence: {score:.4f}")
            print()
            
            if score > 0.5:
                print("✅ DETECTED! (confidence > 0.5)")
            else:
                print("❌ NOT DETECTED (confidence < 0.5)")
            print("=" * 60)
        else:
            print(f"\n⚠️  Warning: Could not find prediction for '{model_name}'")
            print(f"Available predictions: {list(prediction.keys())}")
        
    except ImportError as e:
        print(f"\n❌ Error: Required package not found")
        print(f"Details: {str(e)}")
        print(f"\nPlease install dependencies:")
        print(f"  pip3 install openwakeword pydub numpy")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_model.py <audio_file.wav>")
        print("\nExample:")
        print("  python3 test_model.py test.wav")
        print("  python3 test_model.py dataset/positive/hey_mel_001.wav")
        print("\nThis will test the model at: models/hey_mel.tflite")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model_path = "models/hey_mel.tflite"
    
    test_model(model_path, audio_path)

