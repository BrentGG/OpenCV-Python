import cv2 as cv

if __name__ == '__main__':
    # get video capture
    cap = cv.VideoCapture(1)
    if not cap.isOpened():
        print("Could not open camera")
        exit(-1)

    # get the facial detection cascade
    faceCascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_alt.xml")

    while True:
        success, img = cap.read()
        imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imgGrey = cv.equalizeHist(imgGrey)
        faces = faceCascade.detectMultiScale(imgGrey, 1.3, 5)

        for (x, y, w, h) in faces:
            img = cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.imshow('Cloudy With A Chance Of Meatballs', img)

        # close when q is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
