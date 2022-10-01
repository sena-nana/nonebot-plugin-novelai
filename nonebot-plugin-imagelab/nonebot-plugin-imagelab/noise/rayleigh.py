import cv2
import numpy as np
import matplotlib.pyplot as plt
def gasuss_noise(image, mean=0, var=0.001):
    image = cv2.imread(image)
    image = np.array(image/255, dtype=float)#将原始图像的像素值进行归一化，除以255使得像素值在0-1之间
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    n_rayleigh = -1 * np.power(1-np.log(1 - noise),0.5)
    out = image + n_rayleigh
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)#clip函数将元素的大小限制在了low_clip和1之间了，小于的用low_clip代替，大于1的用1代替
    out = np.uint8(out*255)#解除归一化，乘以255将加噪后的图像的像素值恢复
    #cv.imshow("gasuss", out)
    noise = noise*255
    return [noise,out]
noise,out = gasuss_noise("raw.jpg")
cv2.imwrite('rayleigh.jpg',out)
cv2.imshow('out',out)
plt.hist(out.ravel(), 256, [0, 256])
plt.savefig('rayleigh_plot.png', bbox_inches='tight')
cv2.waitKey(0)