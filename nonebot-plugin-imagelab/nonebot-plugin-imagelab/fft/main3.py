import cv2
import numpy as np
img = cv2.imread("raw5.jpg",0)
W = img.shape[0]
W1 =int(np.power(2,np.ceil(np.log2(W))))
H = img.shape[1]
H1 =int(np.power(2,np.ceil(np.log2(H))))
Wcha=int((W1-W)/2)+1
Hcha=int((H1-H)/2)+1
move=np.float32([[1,0,Wcha],[0,1,Hcha]])
dst=cv2.warpAffine(img,move,(W1,H1))
f = np.fft.fft2(dst)
fshift = np.fft.fftshift(f)
fimg = 5*np.log(np.abs(fshift))
#cv2.imshow("img",fimg)
#cv2.waitKey(0)
#cv2.imwrite("fimg_zero.png",fimg)
