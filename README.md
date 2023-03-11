# Python Computer Vision

Exploring the posibilities of real-time object detection as a way to control an application, using computer vision packages in Python. The projects described below are in chronological order to make some of the progress clearer.

## Cloudy With A Chance Of Meatballs

This project uses OpenCV's built-in real-time facial detection ([docs](https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html)) to play a game. The goal of the game is to catch as many fresh meatballs falling out of the sky in your mouth while avoiding the bad meatballs. A point is scored for every fresh meatball and a point is lost for every bad meatball.

The opencv built-in facial detection works surprisingly well. A problem that is noticeable however, is the relatively slow frame rate. This is due to all the extra computations to make the game work. It is of course also dependent on the hardware that the program is ran on. The facial detection on its own produces an acceptable frame rate. It was also attempted to add mouth detection, this unfortunately reduced the frame rate to an unplayable point. Especially since the mouth detection was a lot less reliable than then face detection (which makes sense since a mouth has a lot less features than a face). Meaning that there were a lot of false positives that had to be eliminated, costing precious resources. So instead an estimation is made of where a mouth would be in relation to the face.

To use your computer's built-in camera, change the line ``cap = cv.VideoCapture(1)`` to ``cap = cv.VideoCapture(0)`` in ``CloudyWithAChanceOfMeatBalls.py``.

A demo:

https://user-images.githubusercontent.com/61016553/224127748-ec0880f5-c8d3-4af7-b2d1-e456e9659a8b.mp4

## Circle Detection

Circle detection using OpenCV caused a lot of problems. The idea was to use circle detection to detect a physical, colored circle and use it as a sort of 'pointer' in multiple projects. However this turned out to be much more of a hassle than expected. the function for circle detection in OpenCV is called ``HoughCircles`` ([docs](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)) and it has a number of parameters that are used to refine the algorithm. A lot of permutations of these parameters, as well as different circular objects and lighting conditions, were tried in an effort to get at least semi-reliable circle detection. As will become clear in the following, this was not achieved.

Probably the most important parameter in ``HoughCircles`` is called ``param2``, it determines how strict the algorithm will be in detecting circles. A lower number gives a higher chance of detecting circles, but also generates a lot of false positives. A higher number will detect less circles but the ones that are detected have a higher probability of actually being circles.

With a ``param2`` of 50 to 70 there are a few false positives, but the circle is not being detected.

![image](https://user-images.githubusercontent.com/61016553/224410868-d752c3b8-2556-49eb-82f9-cc1c97f4361e.png)

Other, more perfectly circular, objects can be detected as long as they are in front of a plain background. Though the detection isn't very reliable.

![image](https://user-images.githubusercontent.com/61016553/224411317-dc911c77-2bcd-488e-8f0b-1b4925c5432a.png)

![image](https://user-images.githubusercontent.com/61016553/224411468-d6a0aabf-6f83-4037-af8a-26b5fb43dae2.png)

A ``param2`` of around 20 to 30 is able to detect the green circle but also produces a lot more false positives, thereby also decreasing the framerate by quite a lot. Detection of the green circle when it was not in front of a plain background was rare. Detection of the weights was more reliable than before.

![image](https://user-images.githubusercontent.com/61016553/224412082-ef16f636-8c80-49b3-af11-7224f3ceabfe.png)

![image](https://user-images.githubusercontent.com/61016553/224414572-71db4138-c398-436f-a6e8-a9011b36c7f6.png)

A high ``param2`` of around 90 to 100 produced almost no false positives but naturally had no chance of detecting the circular object in question.

To make matters worse, detection of the circles always failed once the object moved even slightly, making it useless as a pointer.

In conclusion, circle detection seems to not be the right fit for use as a pointer. It would be better to stick to objects with a lot more clearly defined features, like a face. Facial detection worked a lot better (see [this project](https://github.com/BrentGG/OpenCV-Python#cloudy-with-a-chance-of-meatballs)) than circle detection, but of course it would be unusual to use one's face as a pointer. If a cascade file can be found for hand detection, this might be a better fit.

## Hand Detection using OpenCV

TODO

## Mouse Hands

TODO

## Sources
- [How to Detect Objects in Real-Time Using OpenCV and Python](https://towardsdatascience.com/how-to-detect-objects-in-real-time-using-opencv-and-python-c1ba0c2c69c0)
- [OpenCV-Python tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Mediapipe documentation](https://google.github.io/mediapipe/)

