# Agrex.AI

## Transistor Detection using OpenCV
This repository contains code to detect transistors in an image using OpenCV. The code applies image processing techniques such as Gaussian Blur, thresholding and morphological operations to accurately detect and highlight the transistors in the image.

### Prerequisites
To run this code, you need to have the following software installed:

Python 3
OpenCV (pip install opencv-python)
Numpy (pip install numpy)

### Usage
1. Clone the repository to your local machine.
2. Open the Jupyter Notebook file ObjectDetection.ipynb.
3. In the code, replace the image file path with the path to your own image.
4. Run the code and see the results.

### Code Explanation
The code first loads the image and converts it to grayscale. Then, it applies Gaussian blur to reduce noise. After that, it applies thresholding to create a binary image, and uses morphological operations to remove small white noise. Finally, it finds contours in the binary image and draws rectangles around each transistor.

### Results 

1. Image Used
![image](https://user-images.githubusercontent.com/64553113/216888641-52ea0a73-508f-4d8d-9078-f854e0687a94.png)

2. Cropped Image to Detect Transistor
![image](https://user-images.githubusercontent.com/64553113/216888708-0ae816ca-49eb-4bb6-8269-4c4854efbdf9.png)

3. Gray-Scale Image
![image](https://user-images.githubusercontent.com/64553113/216888824-4f8d769c-ff4d-4a1c-a753-896659f7a9a5.png)

4. Gaussian Blur Image 
![image](https://user-images.githubusercontent.com/64553113/216888898-f559a4eb-6cb2-4324-81d4-827a22efee76.png)

5. Binary Image with threshold 100
![image](https://user-images.githubusercontent.com/64553113/216889001-32f61ce9-56d5-4d75-ab7f-fe042fba3369.png)

6. Binary Image after morphological operations
![image](https://user-images.githubusercontent.com/64553113/216889107-fe0aab4d-d373-4a31-8555-bed2cb0b0327.png)

7. Image with all contours and drwan rectangles around each transistor detected
![image](https://user-images.githubusercontent.com/64553113/216888588-6e3551d3-0ff9-4ac0-9f20-5135f10ee229.png)


## Contributing
If you want to contribute to this project, feel free to create a pull request.





