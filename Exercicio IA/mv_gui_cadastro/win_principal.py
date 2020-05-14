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
from json import dumps


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.pwidth = 640  # 320
        self.pheight = 480  # 240
        faceCrop = ""
        # FullScreenApp(self.window)

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(0)

        # open video source (by default this will try to open the computer webcam)
        self.vid1 = MyVideoCapture(1)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.pwidth, height=self.pheight)
        self.canvas.pack(side="right", fill="both", expand=True)

        self.canvas1 = tkinter.Canvas(window, width=self.pwidth, height=self.pheight)
        self.canvas1.pack(side="left", fill="both", expand=True)

        # Button that lets the user take a snapshot
        # self.btn_snapshot = tkinter.Button(window, text="Photo", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        ret1, frame1 = self.vid1.get_frame1()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            cv2.imwrite("frame1-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame(self.pwidth, self.pheight)
        ret1, frame1 = self.vid1.get_frame1(self.pwidth, self.pheight)
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        if ret1:
            self.photo1 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame1))
            self.canvas1.create_image(0, 0, image=self.photo1, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=1):
        # Open the video source
        if video_source == 0:
            self.vid = cv2.VideoCapture(video_source)
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)
        else:
            self.vid1 = cv2.VideoCapture(video_source)
            if not self.vid1.isOpened():
                raise ValueError("Unable to open video source", video_source)

    def get_frame(self, pwidth, pheight):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            dim = (pwidth, pheight)
            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                # GRAY FRAME
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # DETECT FACES IN FRAME
                faces = face_cascade.detectMultiScale(gray, 1.4, 5)

                # RUN ALL FACES IN FRAME
                for i, (x, y, w, h) in enumerate(faces):

                    # DRAW RECT IN FACE
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    position_faces.append(str(x) + "," + str(y) + "," + str(w) + "," + str(h))

                    # FACE CROP
                    roi_gray = gray[y:y + h, x:x + w]
                    detected_face = frame[int(y):int(y + h), int(x):int(x + w)]  # crop detected face

                    if not detected_face.any():
                        continue

                    # RESIZE FACE CROP TO 48x48
                    resize = cv2.resize(roi_gray, (48, 48))

                    # Indentificação da Pessoa #################################################
                    idf, confidence = recognizer.predict(resize)
                    nameP = "Desconhecido"

                    if confidence > 150:
                        nameP = label_faces[idf - 1].rstrip('\n')

                    cv2.rectangle(frame, (x, y - 22), (x + w, y), (0, 255, 0), -1)
                    cv2.putText(frame, nameP, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                                cv2.LINE_AA)

                    self.vid.sendFace(self, resize, idf)

                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return None, None

    def get_frame1(self, pwidth, pheight):
        if self.vid1.isOpened():
            ret1, frame1 = self.vid1.read()
            x = 35
            y = 5
            w = 45
            h = 20
            cropTermal = frame1[y:y + h, x:x + w]
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 1)
            try:
                custom_config = r'--oem 3 --psm 6'
                termalText = pytesseract.image_to_string(cropTermal, config=custom_config)
            except:
                termalText = "undefine"

            dim = (pwidth, pheight)
            # resize image
            frame1 = cv2.resize(frame1, dim, interpolation=cv2.INTER_AREA)
            if ret1:
                for faces in position_faces:
                    x, y, w, h = faces.split(",")
                    xt = int(x) + 10
                    yt = int(y) - 20
                    wt = int(w) + 45
                    ht = int(h) + 45
                    cv2.rectangle(frame1, (xt, yt), (xt + wt, yt + ht), (255, 255, 255), 2)
                    cv2.rectangle(frame1, (xt, yt - 22), (xt + wt, yt), (255, 255, 255), -1)
                    cv2.putText(frame1, termalText, (xt, yt - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1,
                                cv2.LINE_AA)
                position_faces.clear()
                # Return a boolean success flag and the current frame converted to BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None
        else:
            return None, None

    def sendFace(self, faceCrop, pId):
        base64_string = b64encode(faceCrop).decode('utf-8')
        data = {'id': pId, 'tp': termalText, 'im': base64_string}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            response = requests.post(url+"/api/enviarVisita",
                                     data=json.dumps(data),
                                     headers=headers,
                                     timeout=5)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

            # Release the video source when the object is destroyed

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


global face_cascade
global termalText
global recognizer
global label_faces
global position_faces
global url
url = "http://localhost:8080"
face_cascade = cv2.CascadeClassifier('resource/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("resource/model_face_recognition.xml")
text_file = open("resource/label_face_recognition.txt", "r")
label_faces = text_file.readlines()
position_faces = []
termalText = ""
App(tkinter.Tk(), "Recognition MV")
