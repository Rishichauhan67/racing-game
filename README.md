# RETRO RACER - Simple 80s Arcade Style Racing Game

A nostalgic 2D racing game inspired by classic 80s arcade games like OutRun and Rad Racer, featuring clean retro aesthetics, simple pixel-art style graphics, and procedurally generated retro sound effects.

## 🎮 Simple Retro Features

### **Clean Visual Design**
- **Simple Gradient Background**: Subtle purple-to-pink gradient
- **Straight Road**: Classic top-down view with cyan borders
- **Clean HUD**: Simple text display for score, speed, distance, time, and level
- **Pixel-Perfect Graphics**: Clean, readable retro styling

### **Retro UI Elements**
- **Chunky Pixel Buttons**: RetroButton class with glow effects
- **Mouse & Keyboard Support**: Click buttons or use traditional keyboard controls
- **Simple Animations**: Clean title effects and button interactions

### **Enhanced Game Elements**
- **Player Car**: Realistic orange car with roof, windshield, headlights, and 4 wheels
- **Enemy Cars**: Detailed purple cars with roofs, windows, headlights, and proper wheels
- **Barriers**: Green rectangular obstacles with white stripes
- **Simple Movement**: Straightforward top-down obstacle avoidance with realistic car physics

## 🔊 Synth-Style Sound System

### **Procedural Sound Generation**
- **SynthSounds Class**: Generates authentic 80s-style sound effects
- **Engine Sounds**: Multi-frequency mixing for realistic engine audio
- **UI Beeps**: Different pitched beeps for menu interactions
- **Level Progression**: Audio cues when speed increases
- **Collision Effects**: Dramatic crash sounds

### **Sound Integration**
- **Button Feedback**: Audio response to all UI interactions
- **Ambient Engine**: Occasional engine sounds during gameplay
- **Safe Fallback**: Game runs without sound if audio fails
- **Stereo Output**: All sounds generated in stereo

## 🎯 Gameplay Features

- **Progressive Difficulty**: Speed and obstacle spawn rate increase over time
- **Simple Scoring**: Points for distance traveled and obstacles passed
- **Level System**: Visual level progression
- **Mouse Support**: Full mouse interaction alongside keyboard controls
- **Performance Optimized**: Smooth 60 FPS gameplay

## Controls

- **Left/Right Arrows**: Steer your car
- **Space**: Start game / Restart after game over
- **Escape**: Quit game (from game over screen)
- **Mouse**: Click buttons for menu navigation

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   # Using pip (in virtual environment)
   pip install -r requirements.txt
   
   # Or using system packages (Ubuntu/Debian)
   sudo apt install python3-pygame python3-numpy
   ```

## How to Run

```bash
python3 retro_racer.py
```

## Testing

Run the feature test to verify all enhancements are working:
```bash
python3 test_features.py
```

## Gameplay

- **Objective**: Survive as long as possible while avoiding obstacles
- **Scoring**: +1 point per frame survived, +10 points per obstacle passed
- **Progression**: Speed and obstacle spawn rate increase over time
- **Challenge**: Navigate through purple enemy cars and green barriers
- **Visual Feedback**: HUD shows real-time stats

## Game Elements

### **Visual Design**
- **Player Car**: Realistic orange car with roof, windshield, headlights, and 4 wheels
- **Enemy Cars**: Detailed purple cars with roofs, windows, headlights, and proper wheels
- **Barriers**: Green rectangular obstacles with white stripes
- **Road**: Simple top-down view with cyan borders and pink center line
- **Background**: Subtle purple-to-pink gradient

### **Audio Design**
- **Procedural Generation**: All sounds created mathematically for authentic retro feel
- **Frequency Mixing**: Engine sounds use multiple sine waves
- **Dynamic Volume**: Sound levels adjust based on game events
- **Stereo Effects**: Full stereo sound field

### **Performance**
- **60 FPS Target**: Smooth gameplay on modern systems
- **Simple Rendering**: Clean, efficient drawing routines
- **Memory Management**: Proper cleanup of game objects

## Technical Features

- **Numpy Integration**: Efficient sound generation using numpy arrays
- **Pygame 2.0+**: Modern pygame features and performance
- **Object-Oriented Design**: Clean, maintainable code structure
- **Error Handling**: Graceful fallbacks for missing features
- **Cross-Platform**: Works on Windows, macOS, and Linux

Enjoy the clean retro racing experience with authentic 80s arcade aesthetics! 🕹️✨
