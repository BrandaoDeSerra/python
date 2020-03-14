import cv2 as cv
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.filters import roberts, sobel, scharr, prewitt


img = imread("./arquivos/goat.jpeg", as_gray=True) # carregando imagem
op_sobel = sobel(img)
fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(50, 50))
ax = axes.ravel()
ax[0].imshow(op_sobel, cmap=plt.cm.gray)
ax[0].set_title('Operador de Sobel')

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()





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

plt.bar(list(range(256)),base)
plt.ylabel('Count')
plt.xlabel('Cor')
plt.title('Histogram count gray scale')
plt.ylim(0, 2000)
plt.xlim(0, 255)
plt.show()


