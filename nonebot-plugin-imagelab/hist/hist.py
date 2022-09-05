#-*-coding:utf-8-*-
import numpy as np
import cv2
import matplotlib.pyplot as plt

def calcGrayHist(img):
    rows,cols = img.shape
    img = img.reshape([rows*cols,])#展平
    grayHist = np.zeros([256],np.uint64)#灰度统计向量
    for pixel in range(img.shape[0]):#统计
        grayHist[img[pixel]] += 1
    return grayHist
def calcHist(img,k):
    rows=img.shape[0]
    cols=img.shape[1]
    Hist = np.zeros([256],np.uint64)#统计向量
    for i in range(rows):
        for j in range(cols):
            color=img[i,j,k]
            Hist[img[i,j,k]] += 1
    return Hist

if __name__ == '__main__':
    img = cv2.imread('raw.jpg',0)
    img_rgb = cv2.imread('raw.jpg')
    grayHist = calcGrayHist(img)
    BHist = calcHist(img_rgb,0)
    GHist = calcHist(img_rgb,1)
    RHist = calcHist(img_rgb,2)

    plt.plot(grayHist,label="grayHist")
    plt.xlabel(u'gray level')
    plt.ylabel(u'number of pixels')
    y_max = np.max(grayHist)
    plt.axis([0, 255, 0, y_max])
    plt.show()

    plt.plot(RHist,label="RHist",color="orangered")
    plt.xlabel(u'level')
    plt.ylabel(u'number of pixels')
    y_max = np.max(RHist)
    plt.axis([0, 255, 0, y_max])

    plt.plot(GHist,label="GHist",color="lime")
    plt.xlabel(u'level')
    plt.ylabel(u'number of pixels')
    y_max = np.max(GHist)
    plt.axis([0, 255, 0, y_max])

    plt.plot(BHist,label="BHist",color="dodgerblue")
    plt.xlabel(u'level')
    plt.ylabel(u'number of pixels')
    y_max = np.max(BHist)
    plt.axis([0, 255, 0, y_max])

    plt.legend()
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
