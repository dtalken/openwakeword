#!/bin/bash

# Quick script to install missing dependencies

echo "Installing missing dependencies for OpenWakeWord..."
echo ""

pip3 install audiomentations chardet librosa soundfile scipy

echo ""
echo "✓ Dependencies installed!"
echo ""
echo "Now you can run training:"
echo "  bash train.sh"



