# OpenCV-Python

Exploring some of the features in the OpenCV-Python package. This repo consists of a number of small projects that all use OpenCV in different ways.

## Cloudy With A Chance Of Meatballs

This project uses real time facial detection to play a game. The goal of the game is to catch as many fresh meatballs falling out of the sky in your mouth. Make sure to not eat the meatballs that have gone bad. You get a point for each fresh meatball and lose a point for each bad meatball, try to get as many points in 60 seconds as you can.

The opencv built-in facial detection works surprisingly well. A problem that is noticeable however, is the relatively slow frame rate. This is due to all the extra computations to make the game work. The facial detection on its own produces an acceptable frame rate. It was also attempted to add mouth detection, this unfortunately reduced the frame rate to an unplayable point. Especially since the mouth detection was a lot less reliable than then face detection. Meaning that there were a lot of false positives that had to be eliminated, costing precious resources.

To use your computer's built-in camera, change the line ``cap = cv.VideoCapture(1)`` to ``cap = cv.VideoCapture(0)`` in ``CloudyWithAChanceOfMeatBalls.py``.

A demo:

https://user-images.githubusercontent.com/61016553/224127748-ec0880f5-c8d3-4af7-b2d1-e456e9659a8b.mp4
