import cv2
from datetime import datetime
import configparser
import numpy as np
import boto3
from PIL import Image
from io import BytesIO


def carimboTempo():
    data_e_hora_atual = datetime.now()
    return data_e_hora_atual.strftime('%d/%m/%Y %H:%M:%S')


config = configparser.RawConfigParser()
config.read('config.properties')
pasta_saida_treino = config['FOLDER_TRAIN']['pastaSaidaModel']

print(carimboTempo() + " > Inicio treinamento ")

face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
ids = []
faces = []
indexNamePersons = []
idx = 0
indexName = ""
indexNameAnt = ""
s3 = boto3.client('s3',
                  aws_access_key_id=str(config['AWS']["aws_access_key_id"]),
                  aws_secret_access_key=str(config['AWS']["aws_secret_access_key"]),
                  region_name=str(config['AWS']["region"]))
myBucket = str(config['AWS']["name_bucket"])
list = s3.list_objects(Bucket=myBucket, Prefix='images/')['Contents']
for s3_key in list:
    s3_object = s3_key['Key']
    if s3_object.endswith("/"):
        continue
    indexName = s3_object.split("/")[1]
    if indexNameAnt == "" or indexName != indexNameAnt:
        idx = idx + 1
        indexNamePersons.append(indexName)

    obj = s3.get_object(Bucket=myBucket, Key=s3_object)
    img = Image.open(BytesIO(obj['Body'].read()))
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi_gray = gray
    face = face_cascade.detectMultiScale(gray, 1.4, 5)
    if len(face) > 0:
        for i, (x, y, w, h) in enumerate(face):
            roi_gray = gray[y:y + h, x:x + w]
            resize = cv2.resize(roi_gray, (48, 48))
            faces.append(resize)
            ids.append(idx)
    else:
        print(carimboTempo() + " > ERRO CROP < Folder " + s3_object)
    indexNameAnt = indexName

recognizer.train(faces, np.array(ids))

with open(pasta_saida_treino + "/" + "label_face_recognition.txt", "w") as txt_file:
    for line in indexNamePersons:
        txt_file.write(line + "\n")
recognizer.save(pasta_saida_treino + "/" + "model_face_recognition.xml")

binary_data_label = open('output_model/label_face_recognition.txt', 'rb')
binary_data_model = open('output_model/model_face_recognition.xml', 'rb')

s3.put_object(Body=binary_data_label, Bucket=myBucket, Key='model/label_face_recognition.txt',
              Metadata={'dt': str(carimboTempo())})
s3.put_object(Body=binary_data_model, Bucket=myBucket, Key='model/model_face_recognition.xml',
              Metadata={'dt': str(carimboTempo())})

print(carimboTempo() + " > Fim treinamento ")
