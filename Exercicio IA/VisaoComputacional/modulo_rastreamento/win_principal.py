import time
import tkinter
from PIL import Image
import pytesseract
import PIL.Image
import PIL.ImageTk
import cv2
import requests
from flask import json
from base64 import b64encode
import configparser
import os
from gtts import gTTS
from datetime import datetime
from pygame import mixer  # Load the popular external library


class App:
    def __init__(self, window, window_title, width, height):
        self.window = window
        self.window.title(window_title)
        self.pwidth = width  # 320
        self.pheight = height  # 240
        self.resetTimeout = int(0)
        self.timeRecognition = int(5)
        self.timeRecognitionMultiplo = int(5)
        self.termalText = "undefine"

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(0)

        # open video source (by default this will try to open the computer webcam)
        self.vid1 = MyVideoCapture(1)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.pwidth, height=self.pheight)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.canvas1 = tkinter.Canvas(window, width=self.pwidth, height=self.pheight)
        self.canvas1.pack(side="bottom", fill="both", expand=True)

        self.delay = 10
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        if self.resetTimeout <= 0:
            ret, frame, self.resetTimeout, self.timeRecognition, self.timeRecognitionMultiplo, self.termalText = self.vid.get_frame(
                self.pwidth, self.pheight, self.resetTimeout, self.timeRecognition, self.timeRecognitionMultiplo,
                self.termalText)
            ret1, frame1, self.termalText = self.vid1.get_frame_termal(self.pwidth, self.pheight, self.termalText)
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            if ret1:
                self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
        else:
            ret, frame = self.vid.get_frame_out()
            ret1, frame1,self.termalText = self.vid1.get_frame_termal(self.pwidth, self.pheight, self.termalText)
            if ret:
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            if ret1:
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
            self.resetTimeout = self.resetTimeout - 1
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source):
        # Open the video source
        if video_source == 0:
            self.vid = cv2.VideoCapture(idInputWebcam)
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", idInputWebcam)
        else:
            self.vid1 = cv2.VideoCapture(idInputTermal)
            if not self.vid1.isOpened():
                raise ValueError("Unable to open video source", idInputTermal)

    def get_frame_out(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.flip(frame, 1)
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return None, None

    def get_frame(self, pwidth, pheight, resetTimeout, timeRecognition, timeRecognitionMultiplo, termalText):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv2.flip(frame, 1)
            dim = (pwidth, pheight)
            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                # GRAY FRAME
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                p_x = int(pwidth / 2)
                p_y = int(pheight / 2)
                px = int(p_x / 2)
                py = int(p_y / 2)
                pw = (px + px)
                ph = (py + py) + 50

                # DRAW RECT IN FACE
                cv2.rectangle(frame, (px, py), (px + pw, py + ph), (0, 255, 255), 2)
                gray = gray[py:py + ph, px:px + pw]

                # DETECT FACES IN FRAME
                faces = face_cascade.detectMultiScale(gray, 1.4, 5)

                if len(faces) <= 1:
                    timeRecognitionMultiplo = 5
                    # RUN ALL FACES IN FRAME
                    for i, (x, y, w, h) in enumerate(faces):

                        if timeRecognition > 0:
                            timeRecognition = timeRecognition - 1
                            continue

                        # FACE CROP
                        roi_gray = gray[y:y + h, x:x + w]
                        detected_face = frame[int(y):int(y + h), int(x):int(x + w)]  # crop detected face

                        if not detected_face.any():
                            continue

                        # RESIZE FACE CROP TO 48x48
                        resize = cv2.resize(roi_gray, (48, 48))

                        pName = ""
                        pIdFull = ""
                        # Indentificação da Pessoa #################################################
                        idf = "undefine"
                        if faceRecognition:
                            idf, confidence = recognizer.predict(resize)
                            if confidence <= 150:
                                idf = "undefine"
                            else:
                                pIdFull = label_faces[idf - 1].rstrip('\n')
                                nameP = pIdFull.split("_")[1]
                        try:
                            if termalText != "undefine" and termalText != "":
                                valor = float(termalText)
                                if valor <= 33:
                                    continue
                                temperaturaCritica = float(config['APP_CONFIG']["temperaturaCrítica"])
                                if faceRecognition:
                                    if idf != "undefine":
                                        if valor >= temperaturaCritica:
                                            mixer.music.load('resource/sound/beep.mp3')
                                            mixer.music.play()
                                            self.text_to_speech("Dirigir-se à sala de aferição!")
                                            resetTimeout = 5
                                            timeRecognition = 5
                                        else:
                                            mixer.music.load('resource/sound/ok.mp3')
                                            mixer.music.play()
                                            self.speech_saudacao(nameP)
                                            resetTimeout = 5
                                            timeRecognition = 5
                                        self.sendFace(pIdFull, idOrigem, termalText, resize)
                                    else:
                                        mixer.music.load('resource/sound/beep.mp3')
                                        mixer.music.play()
                                        self.text_to_speech("Dirigir-se à sala de cadastro!")
                                        resetTimeout = 5
                                        timeRecognition = 5
                                else:
                                    if valor >= temperaturaCritica:
                                        mixer.music.load('resource/sound/beep.mp3')
                                        mixer.music.play()
                                        self.text_to_speech("Dirigir-se à sala de aferição!")
                                        resetTimeout = 5
                                        timeRecognition = 5
                                    else:
                                        mixer.music.load('resource/sound/ok.mp3')
                                        mixer.music.play()
                                        self.speech_saudacao("")
                                        resetTimeout = 5
                                        timeRecognition = 5
                                    self.sendFace(pIdFull, idOrigem, termalText, resize)
                                time.sleep(5)
                        except Exception as err:
                            print(f'Other error occurred: {err}')
                            termalText = "undefine"

                else:
                    timeRecognition = 5
                    if timeRecognitionMultiplo > 0:
                        timeRecognitionMultiplo = timeRecognitionMultiplo - 1
                    else:
                        self.text_to_speech("Uma pessoa por vez, por favor!")
                        time.sleep(2)
                        resetTimeout = 5
                        timeRecognitionMultiplo = 5

                return ret, cv2.cvtColor(frame,
                                         cv2.COLOR_BGR2RGB), resetTimeout, timeRecognition, timeRecognitionMultiplo, termalText
            else:
                return ret, None, resetTimeout, timeRecognition, timeRecognitionMultiplo, termalText
        else:
            return None, None, None, None, None, None

    def get_frame_termal(self, pwidth, pheight, termalText):
        if self.vid1.isOpened():
            ret1, frame1 = self.vid1.read()
            x = 35
            y = 5
            w = 45
            h = 20
            cropTermal = frame1[y:y + h, x:x + w]
            #cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 1)

            try:
                custom_config = r'--oem 3 --psm 6'
                termalText = pytesseract.image_to_string(cropTermal, config=custom_config)
            except Exception as err:
                print(f'OCR error occurred: {err}')
                termalText = "undefine"

            xq = 1
            yq = 25
            wq = 313
            hq = 190
            # cv2.rectangle(frame1, (xq, yq), (xq + wq, yq + hq), (0, 255, 255), 1)
            frame1 = frame1[yq:yq + hq, xq:xq + wq]
            frame1 = cv2.flip(frame1, 1)
            dim = (pwidth, pheight)
            # resize image
            frame1 = cv2.resize(frame1, dim, interpolation=cv2.INTER_AREA)
            if ret1:
                # Return a boolean success flag and the current frame converted to BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), termalText
            else:
                return ret1, None, None
        else:
            return None, None, None

    def sendFace(self, pId, pIdOrigem, pTermalText, faceCrop):
        base64_string_face = b64encode(faceCrop).decode('utf-8')
        data = {'id': pId, 'idOrigem': idOrigem, 'tp': pTermalText, 'im': base64_string_face}
        print(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            response = requests.post(pUrl,
                                     data=json.dumps(data),
                                     headers=headers,
                                     timeout=pTimeout)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error API occurred: {http_err}')
        except Exception as err:
            print(f'API connect error occurred: {err}')

    def speech_saudacao(self, pNome):
        saudacao = "um bom dia!"
        data_e_hora_atual = datetime.now()
        hora24HH = data_e_hora_atual.strftime('%H')
        if 12 <= int(hora24HH) < 18:
            saudacao = "uma boa tarde!"
        elif 18 <= int(hora24HH) < 24:
            saudacao = "uma boa noite!"

        if faceRecognition:
            audio = "Bem-vindo " + pNome + "! A MV deseja a você " + saudacao
        else:
            audio = "Bem-vindo! A MV deseja a você " + saudacao

        tts = gTTS(audio, lang='pt-br', slow=False, lang_check=False)
        # Salva o arquivo de audio
        tts.save('audio.mp3')
        # Da play ao audio
        mixer.init()
        mixer.music.load('audio.mp3')
        mixer.music.play()
        os.remove("audio.mp3")
        time.sleep(3)

    def text_to_speech(self, texto):
        audio = texto
        tts = gTTS(audio, lang='pt-br', slow=False, lang_check=False)
        # Salva o arquivo de audio
        tts.save('audio.mp3')
        # Da play ao audio
        mixer.init()
        mixer.music.load('audio.mp3')
        mixer.music.play()
        os.remove("audio.mp3")
        time.sleep(3)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.vid1.isOpened():
            self.vid1.release()
        cv2.destroyAllWindows()


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        self.master.geometry(self._geom)
        self._geom = geom


# ######## MODULO DE IDENTIFICAÇÃO ######## #
global face_cascade
global recognizer
global label_faces
global pUrl
global pTimeout
global idOrigem
global temperaturaCritica
global idInputWebcam
global idInputTermal
global faceRecognition

mixer.init()
mixer.music.load('resource/sound/beep.mp3')
config = configparser.RawConfigParser()
config.read('resource/config.properties')
pUrl = config['APP_CONFIG']["urlApi"]
pTimeout = int(config['APP_CONFIG']["urlApiTimeout"])
idOrigem = config['APP_CONFIG']["idOrigem"]
idInputWebcam = int(config['APP_CONFIG']["idInputWebcam"])
idInputTermal = int(config['APP_CONFIG']["idInputTermal"])
temperaturaCritica = float(config['APP_CONFIG']["temperaturaCrítica"])

if config['APP_CONFIG']["faceRecognition"] == 'True' or config['APP_CONFIG']["faceRecognition"] == 'true':
    faceRecognition = True
else:
    faceRecognition = False
face_cascade = cv2.CascadeClassifier('resource/model/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("resource/model/model_face_recognition.xml")
text_file = open("resource/model/label_face_recognition.txt", "r")
label_faces = text_file.readlines()
App(tkinter.Tk(), "Recognition MV", int(config['APP_CONFIG']["pwidth"]), int(config['APP_CONFIG']["pheight"]))
