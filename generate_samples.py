"""
Dummy generate_samples module to satisfy OpenWakeWord's import requirement.
This is needed when training with pre-recorded clips only (not using Piper TTS).
"""

def generate_samples(*args, **kwargs):
    """
    Dummy function that does nothing.
    OpenWakeWord requires this import but we're using pre-recorded clips.
    """
    pass


