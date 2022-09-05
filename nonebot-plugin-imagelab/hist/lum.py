import  cv2
import numpy as np

def convert(img,a,b):
    dst=img.copy()
    for i in range(300):
        for j in range(300):
            for c in range(3):
                color=img[i,j][c]*a+b
                if color>255:
                    dst[i,j][c]=255
                elif color<0:
                    dst[i,j][c]=0
                else:
                    dst[i,j][c]=color
    return dst
if __name__ == "__main__":
    img=cv2.imread('raw.jpg')
    lum_up=convert(img,1,50)
    cv2.imwrite('lum_up.png', lum_up)
    lum_down=convert(img,1,-50)
    cv2.imwrite('lum_down.png', lum_down)
    con_up=convert(img,1.1,0)
    cv2.imwrite('con_up.png', con_up)
    con_down=convert(img,0.9,0)
    cv2.imwrite('con_down.png', con_down)