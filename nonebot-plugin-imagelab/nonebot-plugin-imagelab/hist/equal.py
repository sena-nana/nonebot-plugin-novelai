import cv2
import numpy as np
import matplotlib.pyplot as plt
# 读入数据
img_path = "raw.jpg"
img = cv2.imread(img_path,0)
imgrgb = cv2.imread(img_path)
# 生成灰度直方统计图
def equal(img):
    graystatic = [0 for i in range(256)]

    width,height = np.shape(img)

    for i in range(width):
        for j in range(height):
            graystatic[img[i,j]]+=1

    gyh = [i/(width*height) for i in graystatic]
# 得到cdf数据
    cdf = gyh
    for i in range(1, 256):
        cdf[i] = cdf[i] + cdf[i-1]

# 直方图均衡化转换
    imgt = np.copy(img)
    for i in range(width):
        for j in range(height):
            imgt[i,j] = img[i,j]*cdf[img[i,j]]
    return imgt
def grayequal(img,imgrgb):
    gray = equal(img)
    width,height = np.shape(img)
    img_out=imgrgb.copy()
    for i in range(width):
        for j in range(height):
            for k in range(3):
                img_out[i,j,k]=imgrgb[i,j,k]/img[i,j]*gray[i,j]
    return img_out
gray=grayequal(img,imgrgb)
cv2.imwrite('grayequal.png', gray)
b, g ,r =cv2.split(imgrgb)
bequal=equal(b)
gequal=equal(g)
requal=equal(r)
merged=cv2.merge([bequal,gequal,requal])
cv2.imwrite('rgbequal.png', merged)