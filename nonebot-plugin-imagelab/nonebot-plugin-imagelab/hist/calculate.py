import cv2
def meancalgray(img):
    rows=img.shape[0]
    cols=img.shape[1]
    Mean = 0
    for i in range(rows):
        for j in range(cols):
            Mean += img[i,j]
    Mean /= rows*cols
    return Mean
def calgray(img,mean):
    rows=img.shape[0]
    cols=img.shape[1]
    Mean = 0
    for i in range(rows):
        for j in range(cols):
            Mean += pow(img[i,j]-mean,2)
    Mean /= rows*cols
    return Mean
def meancal(img,k):
    rows=img.shape[0]
    cols=img.shape[1]
    Mean = 0
    for i in range(rows):
        for j in range(cols):
            Mean += img[i,j,k]
    Mean /= rows*cols
    return Mean
def cal(img,k,mean):
    rows=img.shape[0]
    cols=img.shape[1]
    Mean = 0
    for i in range(rows):
        for j in range(cols):
            Mean += pow(img[i,j,k]-mean,2)
    Mean /= rows*cols
    return Mean
if __name__ == '__main__':
    img = cv2.imread('raw.jpg')
    imggray = cv2.imread('raw.jpg',0)
    graymean=meancalgray(imggray)
    Bmean=meancal(img,0)
    Gmean=meancal(img,1)
    Rmean=meancal(img,2)
    gray=calgray(imggray,graymean)
    B=cal(img,0,Bmean)
    G=cal(img,1,Gmean)
    R=cal(img,2,Rmean)
    print("RGB均值为",Rmean,Gmean,Bmean)
    print("GRAY均值为",graymean)
    print("RGB方差为",R,G,B)
    print("GRAY方差为",gray)