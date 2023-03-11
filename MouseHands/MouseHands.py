import cv2 as cv
import imutils
import ctypes
import mediapipe as mp
import mouse

if __name__ == '__main__':
    # Get screen info
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Get video capture
    cap = cv.VideoCapture(1)  # Change to 0 to use the built-in camera
    if not cap.isOpened():
        print("Could not open camera")
        exit(-1)

    # Mediapipeline stuff
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    border = 1000
    oldIndexFingerTip = None
    pressed = False
    with mp_hands.Hands(model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            # Read and process frame
            success, img = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            img = imutils.resize(img, height=int(screenSize[1] * 0.8))
            img.flags.writeable = False
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            img = cv.flip(img, 1)
            results = hands.process(img)
            img.flags.writeable = True
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                # Draw the hand landmarks.
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                # Move mouse according to finger
                rightIndex = 0 if len(results.multi_hand_landmarks) < 2 or results.multi_handedness[0].classification[0].label == "Right" else 1
                leftIndex = 1 - rightIndex
                indexFingerTip = results.multi_hand_landmarks[rightIndex].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                if oldIndexFingerTip is None or abs(oldIndexFingerTip.x - indexFingerTip.x) >= 0.0025 or abs(oldIndexFingerTip.y - indexFingerTip.y) >= 0.0025:
                    mouse.move(indexFingerTip.x * (screenSize[0] + border) - int(border / 2), indexFingerTip.y * (screenSize[1] + border) - int(border / 2))
                    oldIndexFingerTip = indexFingerTip
                # Click mouse if left hand does clicking motion
                if len(results.multi_hand_landmarks) > 1:
                    indexFingerTip2 = results.multi_hand_landmarks[leftIndex].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    indexFingerMcp2 = results.multi_hand_landmarks[leftIndex].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    if indexFingerTip2.y > indexFingerMcp2.y:
                        if not pressed:
                            mouse.press()
                            pressed = True
                    elif pressed:
                        mouse.release()
                        pressed = False
                elif pressed:
                    mouse.release()
                    pressed = False

            # Show the frame
            cv.imshow('Hand Mouse Control', img)

            # Close when q is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()
