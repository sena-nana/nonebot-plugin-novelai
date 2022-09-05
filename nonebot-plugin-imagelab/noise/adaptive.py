import cv2
import numpy as np
def adaptive(src,row,col,size,maxsize):
    kernalsize=size*2+1
    new = np.zeros([kernalsize,kernalsize])
    new = src[row-size:row+size+1,col-size:col+size+1]
    new=np.sort(new)
    min =new[0,0]
    max=new[kernalsize-1,kernalsize-1]
    med=new[size,size]
    zxy=src[row,col]
    if(med>min).all()and(med<max).all():
        if(zxy>min).all()and(zxy<max).all():
            return zxy
        else:
            return med
    else:
        size+=1
        if(kernalsize<maxsize):
            return adaptive(src,row,col,size,maxsize)
        else:
            return med
def adap(src,ksize=3):
    min=3
    max=7
    maxsize=int(max/2)
    for j in range(3,src.shape[0]-3):
        for i in range(3,src.shape[1]-3):
            src[j,i]=adaptive(src,j,i,1,max)
    return src
def rgb(image):
    r,g,b = cv2.split(image)
    r = adap(r)
    g = adap(g)
    b = adap(b)
    return cv2.merge([r,g,b])
img = cv2.imread('Salt.jpg')
dst=rgb(img)
cv2.imshow("show1",img)
cv2.imshow("show2_3",dst)
cv2.imwrite("adaptive.jpg",dst)
cv2.waitKey(0)
