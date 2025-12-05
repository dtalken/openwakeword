#!/usr/bin/env python3
"""
Fix Windows file locking issue in openwakeword/data.py trim_mmap function.
The memory-mapped file needs to be properly closed before deletion on Windows.
"""
import os
import sys
import shutil

def patch_trim_mmap():
    """Patch openwakeword/data.py to fix Windows file locking in trim_mmap"""
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
        if 'del mmap_features' in content and '# Windows fix' in content:
            print("[OK] OpenWakeWord data.py trim_mmap already patched")
            return True
        
        # Patch: Fix the trim_mmap function to properly close mmap before deletion
        old_code = '''    # Remove old mmaped file
    os.remove(mmap_path)'''
        
        new_code = '''    # Remove old mmaped file (Windows fix: close handles first)
    del mmap_file1, mmap_file2  # Explicitly delete to close file handles
    import gc
    gc.collect()  # Force garbage collection to release file handles
    import time
    # Retry mechanism for Windows file locking
    max_retries = 10
    for retry in range(max_retries):
        try:
            time.sleep(0.5)  # Wait for handles to be released
            os.remove(mmap_path)
            break
        except PermissionError:
            if retry == max_retries - 1:
                raise
            gc.collect()  # Try garbage collection again
            time.sleep(0.5)'''
        
        if old_code in content:
            backup_file = data_file + '.trim_backup'
            if not os.path.exists(backup_file):
                shutil.copy2(data_file, backup_file)
                print(f"[OK] Backed up original to: {backup_file}")
            
            content = content.replace(old_code, new_code)
            
            # Write the patched file
            with open(data_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("=" * 60)
            print("[OK] Successfully patched trim_mmap in data.py!")
            print("=" * 60)
            print(f"[OK] File: {data_file}")
            print(f"[OK] Backup: {backup_file}")
            print("[OK] Windows file locking fix applied")
            return True
        else:
            print("[WARN]  Warning: Could not find expected code pattern to patch")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error patching data.py: {e}")
        return False

if __name__ == '__main__':
    success = patch_trim_mmap()
    if success:
        print("\n[SUCCESS] Patch complete! Training should work now.")
    else:
        print("\n[ERROR] Patch failed.")


