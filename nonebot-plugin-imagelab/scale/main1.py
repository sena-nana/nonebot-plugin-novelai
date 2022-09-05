# --*-- encoding: utf-8 --*--
import numpy as np
import math
import cv2
import os
def cache(img,img_cache):
    vsize=(1080,720)
    for frame_id in np.arange(1, 24):
        print('processing frame {}...'.format(frame_id))
        desImg = np.zeros((1080,720,3),dtype=np.uint8)
        mH=frame_id*10+200
        mW=frame_id*10+100
        th, tw = img.shape[0]*(24-frame_id)/24, img.shape[1]*(24-frame_id)/24
        beta=frame_id/12
        convertMatrix = [[np.cos(beta),-np.sin(beta),0],[np.sin(beta),np.cos(beta),0],[0,0,1]]
        m = [[1,0,-img.shape[0]/2], [0,1,-img.shape[1]/2], [0,0,1]]
        convertMatrix = np.dot(convertMatrix,m)
        convertMatrix_inv = np.linalg.inv(convertMatrix)
        newWidth = int(img.shape[0] * np.cos(beta) + img.shape[1] * np.sin(beta))
        newHeight = int(img.shape[0] * np.sin(beta) + img.shape[1] * np.cos(beta))
        for i in range(vsize[0]):
            for j in range(vsize[1]):
                    scrx=i-mH
                    scry=j-mW
                    corr_x = (scrx+0.5)/th*img.shape[0]-0.5
                    corr_y = (scry+0.5)/tw*img.shape[1]-0.5
                    pos = [int(corr_x-newWidth/2) , int(corr_y-newHeight/2) ,1]
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
                            desImg[i, j, k] = (point3[0]-corr_x)*fr1 + (corr_x-point1[0])*fr2
        img_path = os.path.join(img_cache, 'frame_%05d.jpg'%frame_id)
        cv2.imwrite(img_path, desImg)
def visualize(img_cache,video_out_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vsize=(720,1080)
    out = cv2.VideoWriter(filename=video_out_path, fourcc=fourcc, fps=24, frameSize=vsize)
    for frame_id in np.arange(1, 24):
        print('processing frame {}...'.format(frame_id))
        img_path = os.path.join(img_cache, 'frame_%05d.jpg'%frame_id)
        img = cv2.imread(img_path)
        cv2.namedWindow("cs")
        cv2.imshow("cs",img)
        cv2.waitKey(100)
        out.write(img)
    out.release()
    cv2.destroyAllWindows()

def main():
    src = 'pic/raw_1.jpg'
    pic = cv2.imread(src)
    img_cache = r'cache/'
    video_out_path = r'video.mp4'
    cache(pic,img_cache)
    visualize(img_cache, video_out_path)
if __name__ == '__main__':
    main()