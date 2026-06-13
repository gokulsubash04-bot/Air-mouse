# 🖐️ Gesture-Controlled Virtual Mouse

A Python-based computer vision application that tracks hand landmarks in real-time using a webcam to control your operating system's cursor and execute custom gesture-based keyboard/mouse commands. 

---

## 🚀 Features

- **Real-Time Webcam Feed**: Captures and processes video input with a full-hand skeleton tracking overlay.
- **Natural Mirror Mode**: Flips the video horizontally so hand movements match cursor movements.
- **Rich Controls**:
  - Vertically scrolling pages/documents (Scroll Up and Scroll Down).
  - Minimizing/restoring all active windows.

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
| ✊ **All fingers closed** (fist) | `REOPEN` | **Restore Minimized Windows** | Close all fingers (fist) to restore all minimized windows (`Win + D`). |
| ☝️ **1 finger open** (index) | `SCROLL UP` | **Scroll Page Up** | Raise 1 finger to trigger continuous scroll up. |
| ✋ **5 fingers open** (open hand) | `CLOSE` | **Minimize All Windows** | Open all 5 fingers to minimize all active windows (`Win + D`). |
| ✌️ **2 fingers open** | `SCROLL DOWN` | **Scroll Page Down** | Raise 2 fingers to trigger continuous scroll down. |

- **ESC Key**: Press `ESC` to close the camera window and exit the application safely.

---

## 🗺️ Roadmap & Future Enhancements

- [x] **Cursor Navigation**: Map the coordinate space of the index finger tip to the full screen height and width.
- [x] **Click Detection**: Implement gesture-based clicking via thumb-to-index finger pinching.
- [x] **Scroll Controls**: Add vertical scrolling navigation by raising multiple fingers.
- [x] **Smoothing Filter**: Implement an Exponential Moving Average (EMA) to prevent cursor jitter.
- [x] **Window Actions**: Map window minimization and restore shortcuts to distinct hand gestures.
- [ ] **Drag & Drop**: Implement click-and-hold gestures for moving files/windows.
- [ ] **Right Click**: Add gesture support for simulating right mouse clicks.
