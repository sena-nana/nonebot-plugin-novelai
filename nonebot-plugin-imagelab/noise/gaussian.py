import cv2
import numpy as np
import matplotlib.pyplot as plt
def gasuss_noise(image, mean=0, var=0.001):
    image = cv2.imread(image)
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    #cv.imshow("gasuss", out)
    noise = noise*255
    return [noise,out]
noise,out = gasuss_noise("raw.jpg", mean=0, var=0.003)
cv2.imshow('noise',noise)
cv2.imwrite('gaussian.jpg',out)
cv2.imshow('out',out)
plt.hist(out.ravel(), 256, [0, 256])
plt.savefig('gaussian_plot.png', bbox_inches='tight')
cv2.waitKey(0)