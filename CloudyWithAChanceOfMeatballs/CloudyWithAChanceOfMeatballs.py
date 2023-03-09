import cv2 as cv
import imutils
import ctypes
import time
import random

from Meatball import Meatball

if __name__ == '__main__':
    # Get screen info
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Game data
    duration = 60
    start = time.time()
    score = 0
    meatballs = []
    meatballSpawnDelay = 1
    meatballMaxSpawnRate = 3
    meatballSpawned = time.time()
    meatBallRadius = int(screensize[1] / 54)
    meatBallMinSpeed = int(screensize[1] / 54)
    meatBallMaxSpeed = int(screensize[1] / 36)
    firstDetection = False

    # Get video capture
    cap = cv.VideoCapture(1)  # Change to 0 to use the built-in camera
    if not cap.isOpened():
        print("Could not open camera")
        exit(-1)

    # Get the facial detection cascade
    faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")

    while True:
        # Read frame and detect face
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = imutils.resize(img, height=int(screensize[1] * 0.8))
        imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgGrey = cv.equalizeHist(imgGrey)
        faces = faceCascade.detectMultiScale(imgGrey, 1.3, 5)

        if len(faces) > 0:
            firstDetection = True
            # Draw rectangle around face
            fx, fy, fw, fh = faces[0]
            img = cv.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
            # Estimate mouth position and size and draw rectangle around it
            mw, mh = int(fw * 0.5), int(fw * 0.1)
            mx, my = int((fx + fw / 2) - (mw / 2)), int((fy + fh * 0.8) - (mh / 2))
            img = cv.rectangle(img, (mx, my), (mx + mw, my + mh), (255, 0, 0), 2)

        if time.time() - start < duration:
            # Update game
            i = 0
            while i < len(meatballs):
                meatballs[i].move()
                x, y = meatballs[i].getPosition()
                r = meatballs[i].getRadius()
                # Detect if meatball has been eaten
                if firstDetection and my <= y <= my + mh * 2 and mx <= x <= mx + mw:
                    score += 1 if meatballs[i].isGood() else -1
                    meatballs.pop(i)
                    i -= 1
                else:
                    # Remove if out of screen
                    if y > len(img) + r:
                        meatballs.pop(i)
                        i -= 1
                    else:
                        img = cv.circle(img, (x, y), r, (14, 37, 93) if meatballs[i].isGood() else (0, 85, 56), cv.FILLED)
                i += 1
            img = cv.putText(img, "Score: " + str(score), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 6)
            img = cv.putText(img, "Score: " + str(score), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        else:
            textSize, _ = cv.getTextSize("Game Over", cv.FONT_HERSHEY_SIMPLEX, 2, 8)
            img = cv.putText(img, "Game Over", (int(len(img[0]) / 2) - int(textSize[0] / 2), int(len(img) / 2) - 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 8)
            img = cv.putText(img, "Game Over", (int(len(img[0]) / 2) - int(textSize[0] / 2), int(len(img) / 2) - 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
            textSize, _ = cv.getTextSize("Score: " + str(score), cv.FONT_HERSHEY_SIMPLEX, 2, 8)
            img = cv.putText(img, "Score: " + str(score), (int(len(img[0]) / 2) - int(textSize[0] / 2), int(len(img) / 2) + 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 8)
            img = cv.putText(img, "Score: " + str(score), (int(len(img[0]) / 2) - int(textSize[0] / 2), int(len(img) / 2) + 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)

        if time.time() - meatballSpawned > meatballSpawnDelay:
            for i in range(random.randint(1, meatballMaxSpawnRate)):
                meatballs.append(Meatball(len(img[0]), meatBallRadius, meatBallMinSpeed, meatBallMaxSpeed))
            meatballSpawned = time.time()

        # Show frame
        cv.imshow('Cloudy With A Chance Of Meatballs', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
