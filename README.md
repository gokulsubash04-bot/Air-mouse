# 🖐️ Gesture-Controlled Virtual Mouse

A Python-based computer vision application that tracks hand landmarks in real-time using a webcam and overlays skeleton structures. This project forms the foundation for a gesture-controlled virtual mouse, utilizing OpenCV and MediaPipe.

---

## 🚀 Features

- **Real-Time Webcam Feed**: Captures video input with low latency.
- **Hand Landmarks Detection**: Detects and tracks 21 distinct hand joint points in real-time.
- **Visual Overlays**: Draws hand skeleton connections using MediaPipe's drawing utilities.
- **Mirror Mode**: Flips the video horizontally to feel natural to the user.

---

## 🛠️ Tech Stack & Dependencies

This project is built using:
- **Python 3.x**
- **[OpenCV](https://opencv.org/)** (`opencv-python`): For camera capture, image processing, and display.
- **[MediaPipe](https://google.github.io/mediapipe/)**: High-fidelity hand and finger tracking framework.
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)**: To eventually simulate mouse movement, clicking, and scrolling.
- **[NumPy](https://numpy.org/)**: For mathematical computations and coordinate transformations.

---

## 📦 Installation

To run this project, make sure you have Python installed, then install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## 🎮 How to Use

The main entry point for the application is [test.py](file:///d:/codeing/mouse/test.py).

Run the script using Python:

```bash
python test.py
```

### Controls:
- **ESC Key**: Press `ESC` to close the camera window and exit the application safely.

---

## 🗺️ Roadmap & Future Enhancements

- [ ] **Cursor Navigation**: Map the coordinate space of the detected hand (specifically index finger tip) to the screen width and height.
- [ ] **Click Detection**: Implement gesture-based clicking (e.g., pinching index finger and thumb, or tapping index and middle finger together).
- [ ] **Scroll & Drag**: Add gesture controls for scrolling pages and dragging objects.
- [ ] **Smoothing Filter**: Implement a Kalman Filter or exponential moving average to prevent cursor jitter.
