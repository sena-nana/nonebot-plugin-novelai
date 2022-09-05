import matplotlib.pyplot as plt
import numpy as np
import cv2
def butterworth_notch_resistant_filter(img, uk, vk, radius=10, n=1):
    M, N = img.shape[1], img.shape[0]

    u = np.arange(M)
    v = np.arange(N)

    u, v = np.meshgrid(u, v)

    DK = np.sqrt((u - M//2 + uk)**2 + (v - N//2 - vk)**2)
    D_K = np.sqrt((u - M//2 - uk)**2 + (v - N//2 + vk)**2)
    D0 = radius
    kernel = (1 / (1 + (D0 / (DK+1e-5))**n)) * (1 / (1 + (D0 / (D_K+1e-5))**n))

    return kernel
def spectrum_fft(fft):
    return np.sqrt(np.power(fft.real, 2) + np.power(fft.imag, 2))
img_ori=cv2.imread('sin_noise.jpg',0)
f = np.fft.fft2(img_ori)
fshift = np.fft.fftshift(f)
spectrum_fshift = spectrum_fft(fshift)
spectrum_fshift_n =spectrum_fshift*255
spectrum_log = np.log(1 + spectrum_fshift)
BNRF = 1 - butterworth_notch_resistant_filter(img_ori, radius=10, uk=25, vk=10, n=2.3)
f1shift = fshift * (BNRF)
f2shift = np.fft.ifftshift(f1shift) #对新的进行逆变换
img_new = np.fft.ifft2(f2shift)
img_new = np.abs(img_new)
img_new=img_ori-img_new
plt.figure(figsize=(15, 15))
plt.subplot(221), plt.imshow(img_ori, 'gray'), plt.title('With Sine noise'), plt.xticks([]),plt.yticks([])
plt.subplot(222), plt.imshow(spectrum_log, 'gray'), plt.title('Spectrum'), plt.xticks([]),plt.yticks([])
plt.subplot(223), plt.imshow(BNRF, 'gray'), plt.title('Spectrum'), plt.xticks([]),plt.yticks([])
plt.subplot(224), plt.imshow(img_new, 'gray'), plt.title('Spectrum'), plt.xticks([]),plt.yticks([])
plt.savefig('3denoise.png', bbox_inches='tight')
plt.tight_layout()
plt.show()