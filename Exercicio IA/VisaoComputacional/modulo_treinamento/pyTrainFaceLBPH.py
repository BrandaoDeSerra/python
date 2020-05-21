import numpy as np
import cv2
from datetime import datetime
import os
import configparser
import logging

def carimboTempo():
    data_e_hora_atual = datetime.now()
    return data_e_hora_atual.strftime('%d/%m/%Y %H:%M:%S')


def creatDir(name):
    # CHECK IF FOLDER EXISTS
    if not os.path.exists(f'{name}'):
        # IF NOT, CREATE
        os.makedirs(f'{name}', mode=0o777, exist_ok=False)


config = configparser.RawConfigParser()
config.read('config.properties')

pasta_arq_treinamento = config['FOLDER_TRAIN']["pastaTreino"]
pasta_saida_treino = config['FOLDER_TRAIN']['pastaSaidaModel']

print(carimboTempo() + " > Inicio trenamento ")

face_cascade = cv2.CascadeClassifier('arquivos/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

persons = os.listdir(pasta_arq_treinamento)
ids = []
faces = []
for i, p in enumerate(persons):
    i += 1
    for f in os.listdir(f'{pasta_arq_treinamento}/{p}'):
        img = cv2.imread(f'{pasta_arq_treinamento}/{p}/{f}', 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi_gray = gray
        face = face_cascade.detectMultiScale(gray, 1.4, 5)
        if len(face) > 0:
            for i, (x, y, w, h) in enumerate(faces):
                roi_gray = gray[y:y + h, x:x + w]
                resize = cv2.resize(roi_gray, (48, 48))
                faces.append(resize)
                ids.append(i)
        else:
            print(carimboTempo() + " > ERRO CROP < Folder "+f)
recognizer.train(faces, np.array(ids))
creatDir(pasta_saida_treino)
with open(pasta_saida_treino+"/"+"label_face_recognition.txt", "w") as txt_file:
    for line in persons:
        txt_file.write(line + "\n")
recognizer.save(pasta_saida_treino+"/"+"model_face_recognition.xml")

print(carimboTempo() + " > Fim treinamento ")
