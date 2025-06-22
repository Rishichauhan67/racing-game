#!/usr/bin/env python3
"""
Test script to verify all enhanced features are working
"""
import pygame
import numpy as np
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import pygame
        print("✓ pygame imported successfully")
        
        import numpy as np
        print("✓ numpy imported successfully")
        
        import math, random, time, sys
        print("✓ standard library modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_pygame_init():
    """Test pygame initialization"""
    print("\nTesting pygame initialization...")
    try:
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✓ pygame and mixer initialized successfully")
        
        # Test display
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Test Window")
        print("✓ display initialized successfully")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ pygame initialization error: {e}")
        return False

def test_sound_generation():
    """Test sound generation with numpy"""
    print("\nTesting sound generation...")
    try:
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Generate a simple beep
        sample_rate = 22050
        duration = 0.1
        frequency = 440
        frames = int(duration * sample_rate)
        
        arr = np.zeros((frames, 2), dtype=np.int16)
        for i in range(frames):
            wave = 4096 * np.sin(frequency * 2 * np.pi * i / sample_rate)
            wave = int(wave * 0.3)
            arr[i] = [wave, wave]
        
        sound = pygame.sndarray.make_sound(arr)
        print("✓ sound generation successful")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ sound generation error: {e}")
        return False

def test_retro_racer_import():
    """Test that the main game can be imported"""
    print("\nTesting retro_racer import...")
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the game classes
        from retro_racer import RetroRacer, SynthSounds, RetroButton
        print("✓ retro_racer classes imported successfully")
        
        # Test sound generation
        beep = SynthSounds.generate_beep(880, 0.1, 0.3)
        print("✓ SynthSounds.generate_beep() works")
        
        engine = SynthSounds.generate_engine_sound(100, 0.2, 0.2)
        print("✓ SynthSounds.generate_engine_sound() works")
        
        return True
    except Exception as e:
        print(f"✗ retro_racer import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎮 RETRO RACER - Enhanced Features Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_pygame_init,
        test_sound_generation,
        test_retro_racer_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced RETRO RACER is ready to run!")
        print("\nTo start the game, run:")
        print("python3 retro_racer.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
