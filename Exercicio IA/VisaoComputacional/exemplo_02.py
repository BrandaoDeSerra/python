import numpy as np
import cv2

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('arquivos/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('arquivos/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('arquivos/haarcascade_smile.xml')

while(True):
	_, frame = cap.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

		#smile = smile_cascade.detectMultiScale(gray, 1.3, 5)
		#for (sx,sy,sw,sh) in smile:
			#cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,255,255),2)

	cv2.imshow('frame',frame)

	key = cv2.waitKey(1)

	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()