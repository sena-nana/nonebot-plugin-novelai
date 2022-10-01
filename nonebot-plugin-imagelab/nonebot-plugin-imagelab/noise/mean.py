import numpy as np
from cv2 import cv2

def ArithmeticMeanAlogrithm(image):
    # 算术均值滤波
    new_image = np.zeros(image.shape)
    image = cv2.copyMakeBorder(image,1,1,1,1,cv2.BORDER_DEFAULT)
    for i in range(1,image.shape[0]-1):
        for j in range(1,image.shape[1]-1):
            new_image[i-1,j-1] = np.mean(image[i-1:i+2,j-1:j+2])
    new_image = (new_image-np.min(image))*(255/np.max(image))
    return new_image.astype(np.uint8)
def rgbArithmeticMean(image):
    r,g,b = cv2.split(image)
    r = ArithmeticMeanAlogrithm(r)
    g = ArithmeticMeanAlogrithm(g)
    b = ArithmeticMeanAlogrithm(b)
    return cv2.merge([r,g,b])

def GeometricMeanOperator(roi):
    roi = roi.astype(np.float64)
    p = np.prod(roi)
    return p ** (1 / (roi.shape[0] * roi.shape[1]))
def GeometricMeanAlogrithm(image):
    # 几何均值滤波
    new_image = np.zeros(image.shape)
    image = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_DEFAULT)
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            new_image[i - 1, j - 1] = GeometricMeanOperator(image[i - 1:i + 2, j - 1:j + 2])
    new_image = (new_image - np.min(image)) * (255 / np.max(image))
    return new_image.astype(np.uint8)
def rgbGemotriccMean(image):
    r,g,b = cv2.split(image)
    r = GeometricMeanAlogrithm(r)
    g = GeometricMeanAlogrithm(g)
    b = GeometricMeanAlogrithm(b)
    return cv2.merge([r,g,b])

def Contra_harmonicMeanOperator(roi,q=2):
    roi = roi.astype(np.float64)
    return np.mean((roi)**(q+1))/np.mean((roi)**(q))
def Contra_harmonicMeanAlogrithm(image,q=2):
    # 逆谐波均值滤波
    new_image = np.zeros(image.shape)
    image = cv2.copyMakeBorder(image,1,1,1,1,cv2.BORDER_DEFAULT)
    for i in range(1,image.shape[0]-1):
        for j in range(1,image.shape[1]-1):
            new_image[i-1,j-1] = Contra_harmonicMeanOperator(image[i-1:i+2,j-1:j+2],q)
    new_image = (new_image-np.min(image))*(255/np.max(image))
    return new_image.astype(np.uint8)
def rgbContra_harmonicMean(image,q=2):
    r,g,b = cv2.split(image)
    r = Contra_harmonicMeanAlogrithm(r,q)
    g = Contra_harmonicMeanAlogrithm(g,q)
    b = Contra_harmonicMeanAlogrithm(b,q)
    return cv2.merge([r,g,b])

img = cv2.imread('Salt+Gas.jpg',0)
dst=Contra_harmonicMeanAlogrithm(img)
dst=GeometricMeanAlogrithm(dst)
cv2.imshow("show1",img)
cv2.imshow("show2_3",dst)
cv2.imwrite("SG_hg.jpg",dst)
cv2.waitKey(0)

