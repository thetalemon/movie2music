import cv2
import numpy as np

img = cv2.imread('./aza.png')
COLOR_NAME = ('blue', 'green', 'red')

sums = [img[:,:,ch].sum() for ch in range(img.shape[2])]
maxIndex = sums.index(max(sums))

print(COLOR_NAME[maxIndex])