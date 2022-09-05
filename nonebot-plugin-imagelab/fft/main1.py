import cv2
import numpy as np

img = cv2.imread("raw5.jpg",0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
fimg = 5*np.log(np.abs(fshift))

#cv2.imshow("img",fimg)
#cv2.waitKey(0)
#cv2.imwrite("fimg5.png",fimg)