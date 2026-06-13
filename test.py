import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui
import math

# Disable PyAutoGUI fail-safe to prevent crashes at screen edges
pyautogui.FAILSAFE = False

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=r"D:\codeing\mouse\hand_landmarker.task"
    ),
    num_hands=1,
    running_mode=VisionRunningMode.IMAGE
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
# Action states to prevent repeated key triggers
is_minimized = False

# Helper to calculate Euclidean distance between two landmarks
def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip the frame horizontally for natural (mirror) interaction
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = landmarker.detect(mp_image)
    gesture_text = "NO HAND"

    if result.hand_landmarks:
        hand = result.hand_landmarks[0]
        index_tip = hand[8]



        # Draw hand connections (skeleton) to track all fingers visually
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),                         # Thumb
            (5, 6), (6, 7), (7, 8),                                 # Index
            (9, 10), (10, 11), (11, 12),                            # Middle
            (13, 14), (14, 15), (15, 16),                           # Ring
            (17, 18), (18, 19), (19, 20),                           # Pinky
            (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)              # Palm
        ]
        for start_idx, end_idx in connections:
            start_lm = hand[start_idx]
            end_lm = hand[end_idx]
            sx, sy = int(start_lm.x * w), int(start_lm.y * h)
            ex, ey = int(end_lm.x * w), int(end_lm.y * h)
            cv2.line(frame, (sx, sy), (ex, ey), (0, 255, 255), 2)

        # Draw hand landmark joints (dots)
        for lm in hand:
            lm_x, lm_y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (lm_x, lm_y), 5, (0, 255, 0), -1)

        # Check if individual fingers are open/extended (comparing tip to PIP joint)
        index_open = index_tip.y < hand[6].y
        middle_open = hand[12].y < hand[10].y
        ring_open = hand[16].y < hand[14].y
        pinky_open = hand[20].y < hand[18].y

        # Count how many of the 4 fingers (index, middle, ring, pinky) are open
        open_fingers_count = sum([index_open, middle_open, ring_open, pinky_open])
        
        # Check if thumb is open (distance to index finger base MCP joint landmark 5)
        thumb_dist = get_distance(hand[4], hand[5])
        thumb_open = thumb_dist > 0.08

        # --- Relaxed and Robust Gesture Classification ---
        if open_fingers_count == 0:
            # All fingers closed (fist) -> Reopen (Restore all)
            gesture_text = "REOPEN"
        elif open_fingers_count == 1:
            # 1 finger up -> Scroll Up
            gesture_text = "SCROLL UP"
        elif open_fingers_count == 2:
            # 2 fingers up -> Scroll Down
            gesture_text = "SCROLL DOWN"
        elif open_fingers_count == 4 and thumb_open:
            # 5 fingers open (4 main open + thumb open) -> Close (Minimize all)
            gesture_text = "CLOSE"
        else:
            gesture_text = "NEUTRAL"

        # --- EXECUTE ACTIONS ---



        # 3. Scroll action
        if gesture_text == "SCROLL UP":
            pyautogui.scroll(20)  # Scroll up
        elif gesture_text == "SCROLL DOWN":
            pyautogui.scroll(-20) # Scroll down

        # 4. Close (Minimize all via Win + D) and Reopen (Restore all via Win + D)
        if gesture_text == "CLOSE":
            if not is_minimized:
                pyautogui.hotkey('win', 'd')
                is_minimized = True
        elif gesture_text == "REOPEN":
            if is_minimized:
                pyautogui.hotkey('win', 'd')
                is_minimized = False



        # Display detected gesture on screen
        cv2.putText(
            frame,
            f"GESTURE: {gesture_text}",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
    else:
        # Reset tracking states if hand is completely out of frame
        pass

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()