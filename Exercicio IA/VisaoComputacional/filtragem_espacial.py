import numpy as np
import cv2
from tkinter import messagebox

# função para fazer a correlação simples, movendo a máscara sobre a imagem
def filtrarImagem(img, mascara):
    aresta_n = mascara.shape[0]
    # Tem que ser uma mascara quadrada e ímpar
    if (mascara.shape[0] != mascara.shape[1]) or (aresta_n % 2 == 0):
        messagebox.showinfo('Alerta','Máscara tem que ser quadrada e ímpar !')
        return 'none'
    img_corr = img.copy()
    media_col_linha_mascara = aresta_n * aresta_n
    # Percorre cada pixel da imagem
    for coluna in range(img.shape[0]):
        for linha in range(img.shape[1]):
            try:
                m = 0
                base = int(aresta_n / 2)
                pivo_linha = aresta_n - base - 1
                for col_mascara in range(mascara.shape[0]):
                    pivo_coluna = base - aresta_n + 1
                    for lin_mascara in range(mascara.shape[1]):
                        m += img[coluna + pivo_coluna][linha + pivo_linha] * mascara[col_mascara][lin_mascara]
                        pivo_coluna += 1
                    pivo_linha += 1
                # intensidade do pixel > Média dos valores
                img_corr[coluna][linha] = m / media_col_linha_mascara
            except:
                img_corr[coluna][linha] = 0
    return img_corr


# Imagem -> Carregando imagem num vetor
imagem = cv2.imread('./arquivos/goat.jpeg')

# Mascara -> tem que ser Quadrada de Impar  n x n -> N
filtro_mascara = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

# Executa a função de correlação, imagem e mascara como parametros! ##################
img_com_filtro = filtrarImagem(imagem, filtro_mascara)

if img_com_filtro != 'none':
    # Mostrar imagem
    cv2.imshow('Original', imagem)
    cv2.imshow('Filtro', img_com_filtro)

    # Funções para funcionamento correto ao mostrar a imagem numa janela
    cv2.waitKey(0)
    cv2.destroyAllWindows()
