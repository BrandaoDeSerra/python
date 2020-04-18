import numpy as np
import cv2


# função para fazer a correlação simples, movendo a máscara sobre a imagem
def correlacao(img, img_corr, mascara):
    # Percorre cada pixel da imagem
    for coluna in range(img.shape[0]):
        for linha in range(img.shape[1]):
            m = 0
            try:
                m += img[coluna - 1][linha + 1] * mascara[0][0]
                m += img[coluna][linha + 1] * mascara[0][1]
                m += img[coluna + 1][linha + 1] * mascara[0][2]

                m += img[coluna - 1][linha] * mascara[1][0]
                m += img[coluna][linha] * mascara[1][1]
                m += img[coluna + 1][linha] * mascara[1][2]

                m += img[coluna - 1][linha - 1] * mascara[2][0]
                m += img[coluna][linha - 1] * mascara[2][1]
                m += img[coluna + 1][linha - 1] * mascara[2][2]

                # Faz a média dos valores e guarda como intensidade do pixel
                img_corr[coluna][linha] = m / 9
            except:
                continue
    return img_corr


# Carregando imagem num vetor
img = cv2.imread('./arquivos/goat.jpeg')
img_corr = cv2.imread('./arquivos/goat.jpeg')

# Cria uma máscara
mascara = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

# Executa a função de correlação
img_corr_comum = correlacao(img, img_corr, mascara)

# Mostrar imagem
cv2.imshow('Original', img)
cv2.imshow('Sobel', img_corr_comum)

# Funções para funcionamento correto ao mostrar a imagem numa janela
cv2.waitKey(0)
cv2.destroyAllWindows()
