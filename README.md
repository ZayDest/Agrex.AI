# Agrex.AI

#Transistor Detection using OpenCV
This repository contains code to detect transistors in an image using OpenCV. The code applies image processing techniques such as Gaussian Blur, thresholding and morphological operations to accurately detect and highlight the transistors in the image.

##Prerequisites
To run this code, you need to have the following software installed:

Python 3
OpenCV (pip install opencv-python)
Numpy (pip install numpy)

##Usage
Clone the repository to your local machine.
Open the Jupyter Notebook file ObjectDetection.ipynb.
In the code, replace the image file path with the path to your own image.
Run the code and see the results.

##Code Explanation
The code first loads the image and converts it to grayscale. Then, it applies Gaussian blur to reduce noise. After that, it applies thresholding to create a binary image, and uses morphological operations to remove small white noise. Finally, it finds contours in the binary image and draws rectangles around each transistor.

##Contributing
If you want to contribute to this project, feel free to create a pull request.





