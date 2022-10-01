import cv2
import numpy as np
from numpy.fft import *
def DFT(sig):
    N = sig.size
    V = np.array([[np.exp(-1j*2*np.pi*v*y/N) for v in range(N)] for y in range(N)])
    return sig.dot(V)

def FFT(x):
    N = x.shape[1]
    if N % 2 > 0:
        raise ValueError("size of x must be a power of 2")
    elif N <= 8:
        return np.array([DFT(x[i,:]) for i in range(x.shape[0])])
    else:
        X_even = FFT(x[:,::2])
        X_odd = FFT(x[:,1::2])
        factor = np.array([np.exp(-2j * np.pi * np.arange(N) / N) for i in range(x.shape[0])])
        return np.hstack([X_even + np.multiply(factor[:,:int(N/2)],X_odd),
                               X_even + np.multiply(factor[:,int(N/2):],X_odd)])

def FFT2D(img):
    return FFT(FFT(img).T).T

def FFT_SHIFT(img):
    M,N = img.shape
    M = int(M/2)
    N = int(N/2)
    return np.vstack((np.hstack((img[M:,N:],img[M:,:N])),np.hstack((img[:M,N:],img[:M,:N]))))
img = cv2.imread("raw.jpg", cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#my_fft = abs(FFT_SHIFT(FFT2D(gray)))
fshift = abs(fftshift(fft2(gray)))
#print('distance from numpy.fft: ',np.linalg.norm(my_fft-fshift))
#cv2.imshow('my FFT2D',5*np.log(1+my_fft))
#cv2.imshow('numpy.fft2',5*np.log(1+fshift))
#cv2.waitKey(0)
#cv2.imwrite('my FFT2D.png',5*np.log(1+my_fft))
#cv2.imwrite('numpy.fft2.png',5*np.log(1+fshift))
