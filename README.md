# Touchless

## Project Description
Touchless is an innovative gesture recognition system that transforms hand movements into intuitive mouse controls, enabling a touchless user experience. Designed for accessibility, this project allows users to navigate their digital environment with natural hand gestures, enhancing efficiency and usability.

## Key Features
- **Gesture-Based Control**: Move the cursor, click, scroll, and swipe through simple hand gestures.
- **Real-Time Tracking**: Utilizes advanced computer vision techniques for precise hand detection and tracking.
- **Customizable Sensitivity**: Adjusts gesture recognition sensitivity for a personalized user experience.
- **Multi-Gesture Support**: Recognizes a variety of gestures, offering versatile control.
- **User-Friendly Setup**: Easy to install and use, making it accessible for all skill levels.

## Technologies Used
- **Python**: Primary language for hand-tracking logic.
- **OpenCV**: For real-time computer vision and image processing.
- **MediaPipe**: Employed for hand landmark detection and gesture recognition.
- **PyAutoGUI**: Simulates mouse movements and clicks based on detected gestures.

## Installation Instructions
1. **Clone the repository**:
   ```bash
   git clone https://github.com/RamNathawat/Touchless.git
2. **Navigate to the project directory**:
   ```
   cd Touchless
3. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
4. **Connect your webcam and run the Casual-Touch.py script**:
   ```
   python Casual-Touch.py

## Gesture Controls

### Mouse Movement
- **Index Finger Up**: Move the mouse cursor.

### Clicking
- **Index and Middle Fingers Up**: Click when fingers are close (less than 40 pixels apart).

### Scrolling
- **Index and Middle Fingers Up**: Adjust finger distance to scroll when fingers are apart (40 pixels or more).

### Right Click
- **Four Fingers Up**: Perform a right-click.
  
### Swipe Left
- **Index Finger and Pinky Finger Up**: Perform a left swipe (Ctrl + Left Arrow).

### Swipe Right
- **Pinky and Thumb Up**: Perform a right swipe (Ctrl + Right Arrow).
  
## Additional Notes
- Adjust parameters in the code for optimal performance based on your setup.
- Ensure your webcam is enabled and accessible.
- Feel free to contribute or improve this project!

## Authors

- [@RamNathawat](https://github.com/RamNathawat)

