# 🖐️ Gesture-Controlled Virtual Mouse

A Python-based computer vision application that tracks hand landmarks in real-time using a webcam to control your operating system's cursor and execute custom gesture-based keyboard/mouse commands. 

---

## 🚀 Features

- **Real-Time Webcam Feed**: Captures and processes video input with minimal latency.
- **Natural Mirror Mode**: Flips the video horizontally so hand movements match cursor movements.
- **Exponential Moving Average (EMA) Smoothing**: Smooths cursor coordinates to eliminate muscle jitter and camera fluctuations.
- **Robust Gesture Recognition**: A relaxed gesture classification system that ignores inactive fingers, preventing false negatives.
- **Rich Controls**:
  - Precision cursor hover navigation.
  - Interactive click triggering via pinch gesture.
  - Vertically scrolling pages/documents.
  - Minimizing/maximizing active windows.
  - Browser page back action.

---

## 🛠️ Tech Stack & Dependencies

This project is built using:
- **Python 3.x**
- **[OpenCV](https://opencv.org/)** (`opencv-python`): For camera capture, image processing, and display.
- **[MediaPipe](https://google.github.io/mediapipe/)**: Landmark detection model for precise hand and finger tracking.
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)**: For cross-platform keyboard and mouse hardware simulation.

---

## 📦 Installation

To run this project, make sure you have Python installed, then install the required dependencies:

```bash
pip install opencv-python mediapipe pyautogui
```

---

## 🎮 How to Use

The main entry point for the application is [test.py](file:///d:/codeing/mouse/test.py).

Run the script using Python:

```bash
python test.py
```

### Controls & Gesture Guide:

| Hand Gesture | On-Screen Label | Action Performed | How it Works |
| :--- | :--- | :--- | :--- |
| ☝️ **Index finger up** (middle closed) | `MOVE CURSOR` | **Move Cursor** | The cursor follows your index tip. Mapped directly to your screen space. |
| 🤏 **Index + Thumb pinch** | `CLICK` | **Left Click** | Touch your index tip and thumb tip together to click. You can hold and move to drag. |
| ✌️ **Index + Middle fingers up** | `SCROLL` | **Scroll Webpage** | Raise both fingers. Move hand **up** to scroll up, or **down** to scroll down. |
| 🤙 **Pinky finger up** (index closed) | `SHOW/HIDE DESKTOP` | **Toggle Active Webpage** | Raise only your pinky finger to minimize/restore active browser window (`Win + D`). |
| 👍 **Thumb extended** (index closed) | `GO BACK` | **Go Back in Browser** | Give a thumbs-up to return to the previous page in web browsers (`Alt + Left Arrow`). |

- **ESC Key**: Press `ESC` to close the camera window and exit the application safely.

---

## 🗺️ Roadmap & Future Enhancements

- [x] **Cursor Navigation**: Map the coordinate space of the index finger tip to the full screen height and width.
- [x] **Click Detection**: Implement gesture-based clicking via thumb-to-index finger pinching.
- [x] **Scroll Controls**: Add vertical scrolling navigation by raising multiple fingers.
- [x] **Smoothing Filter**: Implement an Exponential Moving Average (EMA) to prevent cursor jitter.
- [x] **Window & Back Actions**: Map window minimization/page-back shortcuts to distinct hand gestures.
- [ ] **Drag & Drop**: Implement click-and-hold gestures for moving files/windows.
- [ ] **Right Click**: Add gesture support for simulating right mouse clicks.
