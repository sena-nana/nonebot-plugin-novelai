import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def smooth(image, sigma = 1, length = 5):
    k = length // 2
    gaussian = np.zeros([length, length])
    for i in range(length):
        for j in range(length):
            gaussian[i, j] = np.exp(-((i-k) ** 2 + (j-k) ** 2) / (2 * sigma ** 2))
    gaussian /= 2 * np.pi * sigma ** 2
    gaussian = gaussian / np.sum(gaussian)
    W, H = image.shape
    new_image = np.zeros([W - k * 2, H - k * 2])
    for i in range(W - 2 * k):
        for j in range(H - 2 * k):
            new_image[i, j] = np.sum(image[i:i+length, j:j+length] * gaussian)
    new_image = np.uint8(new_image)
    return new_image

def get_gradient_and_direction(image):

    Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    W, H = image.shape
    gradients = np.zeros([W - 2, H - 2])
    direction = np.zeros([W - 2, H - 2])
    for i in range(W - 2):
        for j in range(H - 2):
            dx = np.sum(image[i:i+3, j:j+3] * Gx)
            dy = np.sum(image[i:i+3, j:j+3] * Gy)
            gradients[i, j] = np.sqrt(dx ** 2 + dy ** 2)
            if dx == 0:
                direction[i, j] = np.pi / 2
            else:
                direction[i, j] = np.arctan(dy / dx)
    gradients = np.uint8(gradients)
    return gradients, direction

def NMS(gradients, direction):

    W, H = gradients.shape
    nms = np.copy(gradients[1:-1, 1:-1])
    for i in range(1, W - 1):
        for j in range(1, H - 1):
            theta = direction[i, j]
            weight = np.tan(theta)
            if theta > np.pi / 4:
                d1 = [0, 1]
                d2 = [1, 1]
                weight = 1 / weight
            elif theta >= 0:
                d1 = [1, 0]
                d2 = [1, 1]
            elif theta >= - np.pi / 4:
                d1 = [1, 0]
                d2 = [1, -1]
                weight *= -1
            else:
                d1 = [0, -1]
                d2 = [1, -1]
                weight = -1 / weight

            g1 = gradients[i + d1[0], j + d1[1]]
            g2 = gradients[i + d2[0], j + d2[1]]
            g3 = gradients[i - d1[0], j - d1[1]]
            g4 = gradients[i - d2[0], j - d2[1]]

            grade_count1 = g1 * weight + g2 * (1 - weight)
            grade_count2 = g3 * weight + g4 * (1 - weight)

            if grade_count1 > gradients[i, j] or grade_count2 > gradients[i, j]:
                nms[i - 1, j - 1] = 0
    return nms

def double_threshold(nms, threshold1, threshold2):

    visited = np.zeros_like(nms)
    output_image = nms.copy()
    W, H = output_image.shape
    def dfs(i, j):
        if i >= W or i < 0 or j >= H or j < 0 or visited[i, j] == 1:
            return
        visited[i, j] = 1
        if output_image[i, j] > threshold1:
            output_image[i, j] = 255
            dfs(i-1, j-1)
            dfs(i-1, j)
            dfs(i-1, j+1)
            dfs(i, j-1)
            dfs(i, j+1)
            dfs(i+1, j-1)
            dfs(i+1, j)
            dfs(i+1, j+1)
        else:
            output_image[i, j] = 0

    for w in range(W):
        for h in range(H):
            if visited[w, h] == 1:
                continue
            if output_image[w, h] >= threshold2:
                dfs(w, h)
            elif output_image[w, h] <= threshold1:
                output_image[w, h] = 0
                visited[w, h] = 1

    for w in range(W):
        for h in range(H):
            if visited[w, h] == 0:
                output_image[w, h] = 0
    return output_image

if __name__ == "__main__":
    # code to read image
    image = cv.imread('raw.jpg',0)
    cv.imshow("Original",image)
    smoothed_image = smooth(image)
    cv.imshow("GaussinSmooth(5*5)",smoothed_image)
    gradients, direction = get_gradient_and_direction(smoothed_image)
    nms = NMS(gradients, direction)
    output_image = double_threshold(nms, 40, 100)
    cv.imshow("outputImage",output_image)
    cv.imwrite("dst.jpg",output_image)
    cv.waitKey(0)
