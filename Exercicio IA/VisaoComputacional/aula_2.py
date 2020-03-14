import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np

img = cv.imread('./arquivos/goat.jpeg')

base = list(range(256))
for i in base:
    base[i] = 0

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
coluna = img_gray.shape[0]
linha  = img_gray.shape[1]
for y in range(coluna):
    for x in range(linha):
        base[img_gray[y, x]] = base[img_gray[y, x]] + 1

plt.bar(list(range(256)), base )
plt.ylabel('Count')
plt.xlabel('Cor')
plt.title('Histogram count gray scale')
plt.ylim(0, 2000)
plt.xlim(0, 255)
plt.show()

plt.hist(img_gray.ravel(),256,[0,256])
plt.show()
