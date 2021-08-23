import numpy as np
import cv2
import cv2.aruco as aruco

def detectArUco(image):
    img = image

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict,
                                                          parameters=parameters)

    return corners


image = cv2.imread("F:/finalNTI2/image/test/F_0.jpg")
print(detectArUco(image))