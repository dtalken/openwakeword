#!/usr/bin/env python3
"""
Fix torchaudio compatibility issue with SpeechBrain.
Adds missing list_audio_backends function to torchaudio if it doesn't exist.

This module should be imported BEFORE any speechbrain imports to prevent errors.
Usage: import fix_torchaudio_compat  (before importing speechbrain)
"""
import torchaudio

def patch_torchaudio():
    """Patch torchaudio to add list_audio_backends if missing"""
    if not hasattr(torchaudio, 'list_audio_backends'):
        # The function should return available backends
        # In torchaudio, backends are typically 'soundfile' and 'sox'
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
            
            # If no backends found, return empty list
            return backends
        
        # Add the function to torchaudio module
        torchaudio.list_audio_backends = list_audio_backends
        print("✓ Patched torchaudio: added list_audio_backends()")
        return True
    return False

# Auto-patch on import
patch_torchaudio()

if __name__ == '__main__':
    print("✓ Torchaudio compatibility patch applied")

