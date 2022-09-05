# --*-- encoding: utf-8 --*--

import numpy as np
import math
import cv2
def bi_move(img,mH,mW):
    scrH=img.shape[0]
    scrW=img.shape[1]
    desImg=np.zeros((scrH+mH,scrW+mW,3),dtype=np.uint8)
    for i in range(scrH+mH):
        for j in range(scrW+mW):
            if i-mH>=0 and j-mW>=0:
                scrx=i-mH
                scry=j-mW
                desImg[i,j]=img[scrx,scry]

    return desImg

def bi_rotate(img,angle):
    beta = angle/180 * np.pi
    newWidth = int(img.shape[0] * np.cos(beta) + img.shape[1] * np.sin(beta))
    newHeight = int(img.shape[0] * np.sin(beta) + img.shape[1] * np.cos(beta))
    desImg = np.zeros((newWidth,newHeight,3),dtype=np.uint8)
    desImg1 = np.zeros((newWidth,newHeight,3),dtype=np.uint8)

    convertMatrix = [[np.cos(beta),-np.sin(beta),0],[np.sin(beta),np.cos(beta),0],[0,0,1]]
    m = [[1,0,-img.shape[0]/2], [0,1,-img.shape[1]/2], [0,0,1]]
    convertMatrix = np.dot(convertMatrix,m)
    convertMatrix_inv = np.linalg.inv(convertMatrix) #逆矩阵
    for x in range(newWidth):
        for y in range(newHeight):
            #由于之前是先转换后再加上宽高的一半得到的坐标，所以此处做逆运算时就要先减去宽高的一半
            pos = [int(x-newWidth/2) , int(y-newHeight/2) ,1]
            originPos = np.dot(convertMatrix_inv,pos)
            corr_x=originPos[0]
            corr_y=originPos[1]
            if (img.shape[0] >  corr_x + 1 and img.shape[1] >  corr_y + 1) and (originPos>=0).all():

                point1 = (math.floor(corr_x), math.floor(corr_y))   # 左上角的点
                point2 = (point1[0], point1[1]+1)
                point3 = (point1[0]+1, point1[1])
                point4 = (point1[0]+1, point1[1]+1)
                for k in range(3):
                    fr1=(point2[1]-corr_y)*img[point1[0], point1[1], k] + (corr_y-point1[1])*img[point2[0], point2[1], k]
                    fr2=(point2[1]-corr_y)*img[point3[0], point3[1], k] + (corr_y-point1[1])*img[point4[0], point4[1], k]
                    desImg[x, y, k] = (point3[0]-corr_x)*fr1 + (corr_x-point1[0])*fr2
                    desImg1[x,y,k]=fr1

    return (desImg,desImg1)

def bi_scale(pic,target_size):
    th, tw = target_size[0], target_size[1]
    desImg = np.zeros(target_size, np.uint8)
    desImg1 = np.zeros(target_size, np.uint8)
    for i in range(th):
        for j in range(tw):

            corr_x = (i+0.5)/th*pic.shape[0]-0.5
            corr_y = (j+0.5)/tw*pic.shape[1]-0.5

            point1 = (math.floor(corr_x), math.floor(corr_y))   # 左上角的点
            point2 = (point1[0], point1[1]+1)
            point3 = (point1[0]+1, point1[1])
            point4 = (point1[0]+1, point1[1]+1)
            for k in range(3):
                fr1 = (point2[1]-corr_y)*pic[point1[0], point1[1], k] + (corr_y-point1[1])*pic[point2[0], point2[1], k]
                fr2 = (point2[1]-corr_y)*pic[point3[0], point3[1], k] + (corr_y-point1[1])*pic[point4[0], point4[1], k]
                bi=(point3[0]-corr_x)*fr1 + (corr_x-point1[0])*fr2
                desImg[i, j, k] = bi
                desImg1[i,j,k]=fr1
    return (desImg,desImg1)


def main():
    src = 'pic/raw_1.jpg'
    target_size = (300, 200, 3)
    pic = cv2.imread(src)
    (scale,scale1)=bi_scale(pic, target_size)
    move=bi_move(pic,50,50)
    (rotate,rotate1)=bi_rotate(pic,30)
    cv2.imwrite('pic/new_scale.png', scale)
    cv2.imwrite('pic/new_scale1.png', scale1)
    cv2.imwrite('pic/new_move.png', move)
    cv2.imwrite('pic/new_rotate.png', rotate)
    cv2.imwrite('pic/new_rotate1.png', rotate1)
if __name__ == '__main__':
    main()