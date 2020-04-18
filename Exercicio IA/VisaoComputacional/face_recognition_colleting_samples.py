from turtle import delay

import numpy as np
import cv2

classificador_rosto = cv2.CascadeClassifier('arquivos/haarcascade_frontalface_default.xml')


def extrair_rosto(img):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # tranforma a imagem em preto e branco
    rostos = classificador_rosto.detectMultiScale(gray, 1.3, 5)
    if rostos is ():
        return None
    for (x, y, w, h) in rostos:
        rosto_cortado = gray[y:y + h, x:x + w]
        return rosto_cortado


cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    if extrair_rosto(frame) is not None:
        count += 1
        rosto = cv2.resize(extrair_rosto(frame), (200, 200))

        file_name_path = '/home/brandao/PycharmProjects/python/Exercicio IA/VisaoComputacional/treino/user' + str(
            count) + '.jpg'
        cv2.imwrite(file_name_path, rosto)

        cv2.putText(rosto, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Rosto cortado', rosto)
    else:
        print("Rosto não encontrado")
        pass

    delay(1)
    if cv2.waitKey(1) == 27 or count == 100:
        break

cap.release()
cv2.destroyAllWindows()
print("Exemplos de Treino concluído !!!")
