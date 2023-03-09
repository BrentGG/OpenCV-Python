import cv2 as cv
import imutils
import ctypes
import time

from Meatball import Meatball

if __name__ == '__main__':
    # Game data
    score = 0
    meatballs = []
    meatballSpawnRate = 1
    meatballSpawned = time.time()

    # Get screen info
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Get video capture
    cap = cv.VideoCapture(1)
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

        # Draw rectangle around face
        for (x, y, w, h) in faces:
            img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Update game
        i = 0
        while i < len(meatballs):
            meatballs[i].move()
            if meatballs[i].getPosition()[1] > len(img) + meatballs[i].getRadius():
                meatballs.pop(i)
                i -= 1
                print("removed")
            else:
                img = cv.circle(img, meatballs[i].getPosition(), meatballs[i].getRadius(), (0, 255, 0) if meatballs[i].isGood() else (0, 0, 255), cv.FILLED)
            i += 1

        if time.time() - meatballSpawned > meatballSpawnRate:
            meatballs.append(Meatball(len(img[0])))
            meatballSpawned = time.time()
            print("added")

        # Show frame
        cv.imshow('Cloudy With A Chance Of Meatballs', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
