import numpy as np
import cv2
import os

from keras.models import Model, Sequential
from keras.layers import Input, Convolution2D, ZeroPadding2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from keras.preprocessing import image
from keras.models import model_from_json

def creatDir(name, path='/home/brandao/PycharmProjects/python/Exercicio IA/VisaoComputacional'):
    # CHECK IF FOLDER EXISTS
    if not os.path.exists(f'{path}/{name}'):
        # IF NOT, CREATE
        os.makedirs(f'{path}/{name}', mode=0o777, exist_ok=False)


def saveFace():
    global saveface
    global nome

    saveface = True
    creatDir('train')
    print("Qual o seu nome?")
    name = input()
    nome = name
    creatDir(name, 'train')


def saveImg(img):
    global nome

    qtd = os.listdir(f'train/{nome}')
    cv2.imwrite(f'train/{nome}/{str(len(qtd))}.jpg', img)


def trainData():
    global recognizer
    global trained
    global persons

    trained = True
    persons = os.listdir('train')
    ids = []
    faces = []
    for i, p in enumerate(persons):
        i += 1
        for f in os.listdir(f'train/{p}'):
            img = cv2.imread(f'train/{p}/{f}', 0)
            faces.append(img)
            ids.append(i)
    recognizer.train(faces, np.array(ids))


def loadVggFaceModel():
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(224, 224, 3)))
    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(4096, (7, 7), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(4096, (1, 1), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Convolution2D(2622, (1, 1)))
    model.add(Flatten())
    model.add(Activation('softmax'))

    return model


def ageModel():
    model = loadVggFaceModel()

    base_model_output = Sequential()
    base_model_output = Convolution2D(101, (1, 1), name='predictions')(model.layers[-4].output)
    base_model_output = Flatten()(base_model_output)
    base_model_output = Activation('softmax')(base_model_output)

    age_model_out = Model(inputs=model.input, outputs=base_model_output)

    age_model_out.load_weights("data/age_model_weights.h5")

    return age_model_out


def genderModel():
    model = loadVggFaceModel()

    base_model_output = Sequential()
    base_model_output = Convolution2D(2, (1, 1), name='predictions')(model.layers[-4].output)
    base_model_output = Flatten()(base_model_output)
    base_model_output = Activation('softmax')(base_model_output)

    gender_model_out = Model(inputs=model.input, outputs=base_model_output)

    gender_model_out.load_weights("data/gender_model_weights.h5")

    return gender_model_out


# Nome
nome = ''

saveface = False
savefaceC = 0
reload = True
activate = 0

trained = False
persons = []
face_cascade = cv2.CascadeClassifier('arquivos/haarcascade_frontalface_default.xml')

# load model
emotion_model = model_from_json(open("data/fer2013.json", "r").read())
# load weights
emotion_model.load_weights('data/emotion_model_weights.h5')
emotions = ('Irritado', 'Desgosto', 'Medo', 'Feliz', 'Triste', 'Surpreso', 'Tranquilo')

age_model = ageModel()
gender_model = genderModel()
ages = np.array([i for i in range(0, 101)])
gender = ('Masculino', 'Feminino')

nameP = ""
gen = gender[0]
predicted_age = "0"

recognizer = cv2.face.LBPHFaceRecognizer_create()

cap = cv2.VideoCapture(0)
_, frame = cap.read()

# LOOP
while True:

    # READ FRAME
    if reload:
        _, frame = cap.read()

        # GRAY FRAME
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # DETECT FACES IN FRAME
        faces = face_cascade.detectMultiScale(gray, 1.4, 5)

        # RUN ALL FACES IN FRAME
        for i, (x, y, w, h) in enumerate(faces):

            # DRAW RECT IN FACE
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # FACE CROP
            roi_gray = gray[y:y + h, x:x + w]
            detected_face = frame[int(y):int(y + h), int(x):int(x + w)]  # crop detected face

            if not detected_face.any():
                continue

            # RESIZE FACE CROP TO 48x48
            resize = cv2.resize(roi_gray, (48, 48))
            nameP = ''
            # CHECK IF RECOGNIZER IS TRAINED
            if trained:
                # Indentificação da Pessoa #################################################
                idf, confidence = recognizer.predict(resize)
                nameP = persons[idf - 1]

                cv2.putText(frame, 'Treinado', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, 'Nao treinado', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            # Sentimento #################################################
            predicted_emotion = emotions[6]
            img_pixels = image.img_to_array(resize)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            if 1 == activate:
                predictions = emotion_model.predict(img_pixels)
                max_index = np.argmax(predictions[0])  # find max indexed array
                predicted_emotion = emotions[max_index]

            if 1 == activate:
                try:
                    # age gender data set has 40% margin around the face. expand detected face.
                    margin = 30
                    margin_x = int((w * margin) / 100)
                    margin_y = int((h * margin) / 100)
                    detected_face = frame[int(y - margin_y):int(y + h + margin_y), int(x - margin_x):int(x + w + margin_x)]
                    detected_face = cv2.resize(detected_face, (224, 224))
                    frame_pixels = image.img_to_array(detected_face)
                    frame_pixels = np.expand_dims(frame_pixels, axis=0)
                    frame_pixels /= 255

                    # Idade #################################################
                    if 1 == activate:
                        age_distributions = age_model.predict(frame_pixels)
                        predicted_age = str(int(np.floor(np.sum(age_distributions * ages, axis=1))[0]))

                    # Genero #################################################
                    if 1 == activate:
                        gender_distribution = gender_model.predict(frame_pixels)[0]
                        gender_index = np.argmax(gender_distribution)
                        if gender_index == 0:
                            gen = gender[1]
                        else:
                            gen = gender[0]
                except:
                    None

            cv2.putText(frame, nameP, (int(x), int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            if 1 == activate:
                label = predicted_emotion + " / " + str(gen) + " / " + str(predicted_age) + " anos."
                cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)

            if saveface:
                cv2.putText(frame, str(savefaceC), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                savefaceC += 1
                saveImg(resize)

            if savefaceC > 100:
                savefaceC = 0
                saveface = False

        cv2.putText(frame, 'Pressione espaco para salvar', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imshow('Video', frame)

    key = cv2.waitKey(15)

    # Digite T , comando para treinar
    if key == 116:
        trainData()

    # Digite espaço para Salvar
    if key == 32:
        saveFace()

    # Digite q para sair
    if key & 0xFF == ord('q'):
        break

    # Digite P para extrair as predições
    if key == 112 or activate == 1:
        if reload:
            if activate == 0:
                activate = 1
            else:
                reload = False
                activate = 0
        else:
            reload = True

cap.release()
cv2.destroyAllWindows()
