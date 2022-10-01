import  cv2 as cv
import numpy as np

img1= cv.imread('3.png',0)
img2 = cv.Laplacian(img1,cv.CV_64F)
img2 = 255*(img2 - img2.min())/(img2.max() - img2.min())
img3 = img1+img2
img3 = 255*(img3 - img3.min())/(img3.max() - img3.min())
a = cv.Sobel(img3,cv.CV_64F,1,0)
b = cv.Sobel(img3,cv.CV_64F,0,1)
img4 = np.clip(np.abs(a) + np.abs(b),0,255)
img5 = cv.medianBlur(np.uint8(img4), 5)
img6 = img3*img5
img6 = 255*(img6 - img6.min())/(img6.max() - img6.min())
img7 = img1+img6
img7 = 255*(img7 - img7.min())/(img7.max() - img7.min())
img8 = 1*((img7) **0.5)
img8 = img8 * 16
cv.imwrite('3_out.png', img8)