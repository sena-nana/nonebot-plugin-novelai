import cv2
import numpy as np
import matplotlib.pyplot as plt

def sp_noise(image,prob):
    image = cv2.imread(image)
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()#随机生成0-1之间的数字
            if rdn < prob:#如果生成的随机数小于噪声比例则将该像素点添加黑点，即椒噪声
                output[i][j] = 0
            elif rdn > thres:#如果生成的随机数大于（1-噪声比例）则将该像素点添加白点，即盐噪声
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]#其他情况像素点不变
    return output

out = sp_noise("raw.jpg",0.03)
cv2.imwrite('Salt.jpg',out)
cv2.imshow('out',out)
plt.hist(out.ravel(), 256, [0, 256])
plt.savefig('Salt_plot.png', bbox_inches='tight')
cv2.waitKey(0)