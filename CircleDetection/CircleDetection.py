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

    circles = None
    while True:
        # Read frame and circles
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = imutils.resize(img, height=int(screensize[1] * 0.8))
        imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgGrey = cv.equalizeHist(imgGrey)
        imgGrey = cv.medianBlur(imgGrey, 5)
        circles = cv.HoughCircles(imgGrey, cv.HOUGH_GRADIENT, 1, 100, param1=50, param2=70, minRadius=10, maxRadius=100)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            print(len(circles))
            if len(circles) < 50:
                for (x, y, r) in circles:
                    img = cv.circle(img, (x, y), r, (255, 0, 255), 2)

        # Show frame
        cv.imshow('Virtual Canvas', img)

        # Close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
