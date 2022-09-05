import cv2
import numpy as np

img = cv2.imread('raw.jpg')

def laplace(img):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])

    dst = cv2.filter2D(img, -1, kernel)
    return dst
def laplace_8(img):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])

    dst = cv2.filter2D(img, -1, kernel)
    return dst
def sobel(img):
    y = np.array([[1, 2, 1],[0, 1, 0],[-1, -2, -1]])
    x = np.array([[1, 0, -1],[2, 1, -2],[1, 0, -1]])
    dsty=cv2.filter2D(img,-1,y)
    dstx=cv2.filter2D(img,-1,x)
    absX = cv2.convertScaleAbs(dstx)
    absY = cv2.convertScaleAbs(dsty)
    Sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Sobel
def sobel_5(img):
    y = np.array([[1,4,6,4,1],[2,8,12,8,2],[0,0,1,0,0],[-2,-8,-12,-8,-2],[-1,-4,-6,-4,-1]])
    x = np.transpose(y)
    dsty=cv2.filter2D(img,-1,y)
    dstx=cv2.filter2D(img,-1,x)
    absX = cv2.convertScaleAbs(dstx)
    absY = cv2.convertScaleAbs(dsty)
    Sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Sobel

dst = laplace(img)
cv2.imshow('dst', dst)
cv2.waitKey(1000)
cv2.imwrite('laplace.jpg', dst)

dst = laplace_8(img)
cv2.imshow('dst', dst)
cv2.waitKey(1000)
cv2.imwrite('laplace_8.jpg', dst)

dst = sobel(img)
cv2.imshow('dst', dst)
cv2.waitKey(1000)
cv2.imwrite('sobel.jpg', dst)

dst = sobel_5(img)
cv2.imshow('dst', dst)
cv2.waitKey(1000)
cv2.imwrite('sobel_5.jpg', dst)
