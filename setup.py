"""
Setup Script for Text to Audio Converter
Run this first to install dependencies and create folders
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 50)
    print("TEXT TO AUDIO CONVERTER - SETUP")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Step 1: Install dependencies
    print("\n[1/3] Installing required packages...")
    print("-" * 30)
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages. Please run manually:")
        print("  pip install -r requirements.txt")
    
    # Step 2: Create folders
    print("\n[2/3] Creating folder structure...")
    print("-" * 30)
    
    folders = ["input", "output"]
    for folder in folders:
        folder_path = current_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"✓ Created folder: {folder_path}")
    
    # Step 3: Test TTS engine
    print("\n[3/3] Testing Text-to-Speech engine...")
    print("-" * 30)
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"✓ TTS engine working! Found {len(voices)} voice(s)")
        
        # Create a test file. The "_en" suffix tells the converter to use an
        # English voice (language is chosen per file from this suffix).
        test_file = current_dir / "input" / "test_en.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Hello! This is a test file. If you can hear this, the converter is working correctly.")
        print(f"✓ Created test file: {test_file}")
        
    except Exception as e:
        print(f"✗ TTS engine test failed: {e}")
        print("  You may need to install additional system components.")
    
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Place your text files in the 'input' folder")
    print("2. Run: python main.py")
    print("3. Find your audio files in the 'output' folder")
    print("\nTo customize settings, edit the configuration section in main.py")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()