#!/usr/bin/env python3
"""
Patch speechbrain to fix torchaudio compatibility issue.
This patches the torch_audio_backend.py file to handle missing list_audio_backends.
"""
import os
import shutil

def patch_speechbrain():
    """Patch speechbrain's torch_audio_backend.py for torchaudio compatibility"""
    try:
        import sys
        # Find site-packages directory without importing speechbrain
        site_packages = None
        for path in sys.path:
            if 'site-packages' in path and os.path.isdir(path):
                site_packages = path
                break
        
        if not site_packages:
            print("[ERROR] Error: Could not find site-packages directory")
            return False
        
        speechbrain_dir = os.path.join(site_packages, 'speechbrain')
        backend_file = os.path.join(speechbrain_dir, 'utils', 'torch_audio_backend.py')
        
        if not os.path.exists(backend_file):
            print(f"[ERROR] Error: Could not find {backend_file}")
            return False
        
        # Backup original file
        backup_file = backend_file + '.original_backup'
        if not os.path.exists(backup_file):
            shutil.copy2(backend_file, backup_file)
            print(f"[OK] Backed up original to: {backup_file}")
        
        # Read the file
        with open(backend_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if 'hasattr(torchaudio, "list_audio_backends")' in content:
            print("[OK] SpeechBrain already patched for torchaudio compatibility")
            return True
        
        # Patch: Add hasattr check before list_audio_backends calls
        old_code1 = '''    elif torchaudio_major >= 2 and torchaudio_minor >= 1:
        available_backends = torchaudio.list_audio_backends()'''
        
        new_code1 = '''    elif torchaudio_major >= 2 and torchaudio_minor >= 1:
        # Compatibility fix: some torchaudio versions don't have list_audio_backends
        if not hasattr(torchaudio, 'list_audio_backends'):
            return  # Skip backend check if function doesn't exist
        available_backends = torchaudio.list_audio_backends()'''
        
        old_code2 = '''            torchaudio.list_audio_backends(),'''
        
        new_code2 = '''            torchaudio.list_audio_backends() if hasattr(torchaudio, 'list_audio_backends') else [],'''
        
        patched = False
        if old_code1 in content:
            content = content.replace(old_code1, new_code1)
            patched = True
        
        if old_code2 in content:
            content = content.replace(old_code2, new_code2)
            patched = True
        
        if patched:
            
            # Write the patched file
            with open(backend_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("=" * 60)
            print("[OK] Successfully patched SpeechBrain!")
            print("=" * 60)
            print(f"[OK] File: {backend_file}")
            print(f"[OK] Backup: {backup_file}")
            print("[OK] Torchaudio compatibility fix applied")
            return True
        else:
            print("[WARN]  Warning: Could not find expected code pattern to patch")
            print("The file structure may have changed. Manual patching required.")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error patching speechbrain: {e}")
        return False

if __name__ == '__main__':
    success = patch_speechbrain()
    if success:
        print("\n[SUCCESS] Patch complete! You can now run training.")
    else:
        print("\n[ERROR] Patch failed. Please check the error messages above.")


