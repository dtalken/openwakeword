#!/usr/bin/env python3
"""
Fix torchaudio backend to use soundfile instead of torchcodec.
This avoids the FFmpeg dependency issue on Windows.
"""
import os
import sys

def patch_openwakeword_data():
    """Patch openwakeword/data.py to use soundfile backend"""
    try:
        # Find site-packages
        site_packages = None
        for path in sys.path:
            if 'site-packages' in path and os.path.isdir(path):
                site_packages = path
                break
        
        if not site_packages:
            print("[ERROR] Error: Could not find site-packages directory")
            return False
        
        data_file = os.path.join(site_packages, 'openwakeword', 'data.py')
        
        if not os.path.exists(data_file):
            print(f"[ERROR] Error: Could not find {data_file}")
            return False
        
        # Read the file
        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already patched
        if 'backend="soundfile"' in content:
            print("[OK] OpenWakeWord data.py already patched")
            return True
        
        # Patch: Replace torchaudio.load calls to use soundfile backend
        old_code = 'clip_data, clip_sr = torchaudio.load(clip)'
        new_code = 'clip_data, clip_sr = torchaudio.load(clip, backend="soundfile")'
        
        if old_code in content:
            import shutil
            backup_file = data_file + '.backend_backup'
            if not os.path.exists(backup_file):
                shutil.copy2(data_file, backup_file)
                print(f"[OK] Backed up original to: {backup_file}")
            
            content = content.replace(old_code, new_code)
            
            # Write the patched file
            with open(data_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("=" * 60)
            print("[OK] Successfully patched OpenWakeWord data.py!")
            print("=" * 60)
            print(f"[OK] File: {data_file}")
            print(f"[OK] Backup: {backup_file}")
            print("[OK] Torchaudio backend set to 'soundfile'")
            return True
        else:
            print("[WARN]  Warning: Could not find expected code pattern to patch")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error patching openwakeword/data.py: {e}")
        return False

if __name__ == '__main__':
    success = patch_openwakeword_data()
    if success:
        print("\n[SUCCESS] Patch complete! Training should now work without FFmpeg.")
    else:
        print("\n[ERROR] Patch failed.")


