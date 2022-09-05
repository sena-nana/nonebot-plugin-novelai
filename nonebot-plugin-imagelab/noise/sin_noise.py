import numpy as np
import cv2
def add_sin_noise(img, scale=1, angle=0):
    height, width = img.shape[:2]
    if int(angle / 90) % 2 == 0:
        rotate_angle = angle % 90
    else:
        rotate_angle = 90 - (angle % 90)
    rotate_radian = np.radians(rotate_angle)

    new_height = int(np.ceil(height * np.cos(rotate_radian) + width * np.sin(rotate_radian)))
    new_width = int(np.ceil(width * np.cos(rotate_radian) + height * np.sin(rotate_radian))) 

    if new_height < height:
        new_height = height
    if new_width < width:
        new_width = width

    u = np.arange(new_width)
    v = np.arange(new_height)
    u, v = np.meshgrid(u, v)
    noise = 1 - np.sin(u * scale)

    C1 = cv2.getRotationMatrix2D((new_width/2.0, new_height/2.0), angle, 1)
    new_img = cv2.warpAffine(noise, C1, (int(new_width), int(new_height)), borderValue=0)

    offset_height = abs(new_height - height) // 2
    offset_width = abs(new_width - width) // 2
    img_dst = new_img[offset_height:offset_height + height, offset_width:offset_width+width]

    return img_dst
img=cv2.imread("raw.jpg",0)
noise=add_sin_noise(img,0.3,30)/10
img = np.array(img / 255, np.float32)
img_noise = img + noise
cv2.imwrite('sin_noise.jpg',img_noise*255)
cv2.imshow("img_noise",img_noise)
cv2.waitKey(0)