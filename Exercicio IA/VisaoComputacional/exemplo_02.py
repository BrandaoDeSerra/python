import numpy as np
import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('arquivos/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('arquivos/haarcascade_eye.xml')

while(True):
	conectado, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #tranforma a imagem em preto e branco
	# cv2.imshow('gray', gray)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		#cv2.imshow('roi_gray', roi_gray)
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),2)

	cv2.imshow('Visao Computacional',frame)

	key = cv2.waitKey(1)

	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()