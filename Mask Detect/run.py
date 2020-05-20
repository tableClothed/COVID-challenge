import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import dlib
import imutils
from imutils import face_utils
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

p = "data/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

offset = 40

model = load_model("models/MobileNetV2.h5")
camera = cv2.VideoCapture(0)


def crop_face(img):
	face, face1 = 0, 0
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	for rect in rects:
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		y2 = shape[8][1] + offset  # chin
		y1 = shape[19][1] - offset # eyebrow
		x1 = shape[0][0] - offset  # left cheek
		x2 = shape[16][0] + offset # right cheek

		w, h = x2 - x1, y2 - y1

		face = img[y1:y1+h, x1:x1+w]

		face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
		face1 = cv2.resize(face, (224, 224))
		face = img_to_array(face1)
		face = preprocess_input(face)
		face = np.expand_dims(face, axis=0)

	return face, face1



while True:
	_, frame = camera.read()

	face, face1 = crop_face(frame)

	try:
		mask, without_mask = model.predict(face)[0]
	except:
		mask, without_mask = 0, 0

	text = "Mask" if mask > without_mask else "No mask"
	color = (0, 255, 0) if text == "Mask" else (0, 0, 255)

	text += f": {max(mask, without_mask)*100}%"
	frame = cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

	cv2.imshow("face", face1)

	cv2.imshow("frame", frame)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break


cv2.destroyAllWindows()
camera.release()