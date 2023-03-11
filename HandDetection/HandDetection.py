import cv2 as cv
import numpy as np
import imutils
import ctypes

if __name__ == '__main__':
    # Get screen info
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Get video capture
    cap = cv.VideoCapture(1)  # Change to 0 to use the built-in camera
    if not cap.isOpened():
        print("Could not open camera")
        exit(-1)

    # Get the facial detection cascade
    cascade = cv.CascadeClassifier("closed_frontal_palm1.xml")

    circles = None
    while True:
        # Read frame and circles
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = imutils.resize(img, height=int(screensize[1] * 0.8))
        img = cv.medianBlur(img, 5)
        imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgGrey = cv.equalizeHist(imgGrey)
        objects = cascade.detectMultiScale(imgGrey, 1.3, 5)
        print(len(objects))
        for (x, y, w, h) in objects:
            img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Show frame
        cv.imshow('Virtual Canvas', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
