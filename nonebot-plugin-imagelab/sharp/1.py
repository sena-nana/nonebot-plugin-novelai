import numpy as np
import cv2

img = cv2.imread('raw.jpg')

def Blur(img,n,m=0):
    if m==0:
        kernal = np.ones((n,n), np.float32)/pow(n,2)
    elif m==1:
        kernal = np.array([[0,1,0],[1,0,1],[0,1,0]],np.float32)/4
    else:
        kernal = np.array([[1,0,1],[0,1,0],[1,0,1]],np.float32)/5
    dst = cv2.filter2D(img, -1, kernal)
    return dst

def Median(img,k=3):
    imarray=img
    height = imarray.shape[0]
    width = imarray.shape[1]
    edge = int((k - 1) / 2)
    new_arr = np.zeros((height, width), dtype="uint8")
    for i in range(edge,height-edge):
        for j in range(edge,width-edge):
            new_arr[i, j] = np.median(imarray[i - edge:i + edge + 1, j - edge:j + edge + 1])# 调用np.median求取中值
    return new_arr

def MedianF(img,k=3):
    (B, G, R) = cv2.split(img)
    B1=Median(B,k)
    G1=Median(G,k)
    R1=Median(R,k)
    return cv2.merge([B1,G1,R1])

b3l = Blur(img,3)
cv2.imshow("imgs",b3l)
cv2.waitKey(1000)
cv2.imwrite("Blur3x3.jpg",b3l)

b5l = Blur(img,5)
cv2.imshow("imgs",b5l)
cv2.waitKey(1000)
cv2.imwrite("Blur5x5.jpg",b5l)

b7l = Blur(img,7)
cv2.imshow("imgs",b7l)
cv2.waitKey(1000)
cv2.imwrite("Blur7x7.jpg",b7l)

b3l_1 = Blur(img,3,1)
cv2.imshow("imgs",b3l_1)
cv2.waitKey(1000)
cv2.imwrite("Blur3x3_1.jpg",b3l_1)

b3l_2 = Blur(img,3,2)
cv2.imshow("imgs",b3l_2)
cv2.waitKey(1000)
cv2.imwrite("Blur3x3_2.jpg",b3l_2)

m3l = MedianF(img,3)
cv2.imshow("imgs",m3l)
cv2.waitKey(1000)
cv2.imwrite("Median3x3.jpg",m3l)

m5l = MedianF(img,5)
cv2.imshow("imgs",m5l)
cv2.waitKey(1000)
cv2.imwrite("Median5x5.jpg",m5l)