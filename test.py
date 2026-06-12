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
screen_w, screen_h = pyautogui.size()

# Smoothing configuration (Exponential Moving Average)
SMOOTHING = 0.15
prev_x, prev_y = None, None

# Action states to prevent repeated key triggers
clicked = False
desktop_toggled = False
back_triggered = False
prev_scroll_y = None

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

        # Calculate visual coordinates on the frame
        x = int(index_tip.x * w)
        y = int(index_tip.y * h)

        # Check if individual fingers are open/extended (comparing tip to PIP joint)
        index_open = index_tip.y < hand[6].y
        middle_open = hand[12].y < hand[10].y
        pinky_open = hand[20].y < hand[18].y
        
        # For thumb: check distance to index finger base MCP joint (landmark 5)
        thumb_dist = get_distance(hand[4], hand[5])
        thumb_open = thumb_dist > 0.08

        # Check pinch distance between thumb tip and index tip for Click
        pinch_dist = get_distance(hand[4], index_tip)
        is_pinch = pinch_dist < 0.045

        # --- Relaxed and Robust Gesture Classification ---
        if is_pinch:
            # Pinch gesture takes priority for click, regardless of finger extension states
            gesture_text = "CLICK"
        elif index_open and middle_open:
            # Index and Middle fingers both open -> Scroll mode
            gesture_text = "SCROLL"
        elif index_open and not middle_open:
            # Index open, Middle closed -> Cursor control (either Move or Click)
            gesture_text = "MOVE CURSOR"
        elif pinky_open and not index_open:
            # Pinky open, Index closed -> Toggle desktop (Hide/Show webpage)
            gesture_text = "SHOW/HIDE DESKTOP"
        elif thumb_open and not index_open:
            # Thumb open, Index closed -> Go Back
            gesture_text = "GO BACK"
        else:
            gesture_text = "NEUTRAL"

        # --- EXECUTE ACTIONS ---

        # 1. Move Cursor (works in both MOVE CURSOR and CLICK states for precise clicking)
        if gesture_text in ["MOVE CURSOR", "CLICK"]:
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

            # Scale coordinates using the entire camera space
            norm_x = max(0.0, min(1.0, index_tip.x))
            norm_y = max(0.0, min(1.0, index_tip.y))

            target_x = int(norm_x * screen_w)
            target_y = int(norm_y * screen_h)

            if prev_x is None or prev_y is None:
                smooth_x, smooth_y = target_x, target_y
            else:
                smooth_x = int(prev_x + (target_x - prev_x) * SMOOTHING)
                smooth_y = int(prev_y + (target_y - prev_y) * SMOOTHING)

            prev_x, prev_y = smooth_x, smooth_y

            mouse_x = max(0, min(screen_w - 1, smooth_x))
            mouse_y = max(0, min(screen_h - 1, smooth_y))
            pyautogui.moveTo(mouse_x, mouse_y)

        # 2. Click action
        if gesture_text == "CLICK":
            if not clicked:
                pyautogui.click()
                clicked = True
        else:
            # Reset click state when pinch is released
            if pinch_dist >= 0.055:
                clicked = False

        # 3. Scroll action
        if gesture_text == "SCROLL":
            cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

            if prev_scroll_y is None:
                prev_scroll_y = index_tip.y
            else:
                dy = index_tip.y - prev_scroll_y
                # If dy is negative, finger moved up -> scroll up (positive value)
                # If dy is positive, finger moved down -> scroll down (negative value)
                scroll_amount = -int(dy * 1200)
                if abs(scroll_amount) >= 1:
                    pyautogui.scroll(scroll_amount)
                    prev_scroll_y = index_tip.y
        else:
            prev_scroll_y = None

        # 4. Hide/Show webpage (Toggle Desktop via Win + D)
        if gesture_text == "SHOW/HIDE DESKTOP":
            if not desktop_toggled:
                pyautogui.hotkey('win', 'd')
                desktop_toggled = True
        else:
            desktop_toggled = False

        # 5. Go Back (Alt + Left Arrow)
        if gesture_text == "GO BACK":
            if not back_triggered:
                pyautogui.hotkey('alt', 'left')
                back_triggered = True
        else:
            back_triggered = False

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
        prev_x, prev_y = None, None
        prev_scroll_y = None
        clicked = False
        desktop_toggled = False
        back_triggered = False

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()