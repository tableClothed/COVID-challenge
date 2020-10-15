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

# p = "data/shape_predictor_68_face_landmarks.dat"
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(p)
# face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye.xml')
# eye_cascade = cv2.CascadeClassifier('data/haarcascade_eye_tree_eyeglasses.xml')
upper_cascade = cv2.CascadeClassifier('data/haarcascade_upperbody.xml')

offset = 40

model = load_model("models/MobileNetV2.h5")
camera = cv2.VideoCapture(0)


# BAD IDEA
# because mask covers face points

# def crop_face(img):
# 	face, face1 = 0, 0
# 	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 	rects = detector(gray, 0)
# 	for rect in rects:
# 		shape = predictor(gray, rect)
# 		shape = face_utils.shape_to_np(shape)

# 		y2 = shape[8][1] + offset  # chin
# 		y1 = shape[19][1] - offset # eyebrow
# 		x1 = shape[0][0] - offset  # left cheek
# 		x2 = shape[16][0] + offset # right cheek

# 		w, h = x2 - x1, y2 - y1

# 		face = img[y1:y1+h, x1:x1+w]

# 		face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
# 		face1 = cv2.resize(face, (224, 224))
# 		face = img_to_array(face1)
# 		face = preprocess_input(face)
# 		face = np.expand_dims(face, axis=0)

# 	return face, face1
# face1 is for debugging



# BAD IDEA
# pretty much the same reason as above

def crop_face(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
		face = frame[y:y+h, x:x+w]
		face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
		face1 = cv2.resize(face, (224, 224))
		face = img_to_array(face1)
		face = preprocess_input(face)
		face = np.expand_dims(face, axis=0)
	return face



# def crop_face(frame):
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 	eye = eye_cascade.detectMultiScale(gray, 1.3, 2)[0]
# 	(x1, y1, w1, h1) = eyes[0]
# 	eye_centre  = (x1 + x1 + w1//2, y1 + y1 + h1//2)

# 	(x2, y2, w2, h2) = eyes[1]
# 	eye2_centre  = (x2 + x2 + w2//2, y2 + y2 + h2//2)

# 	centre_x = int(abs(eye1_centre[0] + eye2_centre[0])/2)
# 	centre_y = int(abs(eye1_centre[1] + eye2_centre[1])/2)

# 	# eyes width is like 1/5 of face
# 	margin_x = int(abs((w1+w2)/2)*3)
# 	margin_y = int(abs((h1+h2)/2)*8)


# 	eyes_centre = (centre_x, centre_y)

# 	for (x, y, w, h) in faces:
# 		face = frame[y-margin_y:y-margin_y+h, x--margin_x:x-margin_x+w]
# 		face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
# 		face1 = cv2.resize(face, (224, 224))
# 		face = img_to_array(face1)
# 		face = preprocess_input(face)
# 		face = np.expand_dims(face, axis=0)
# 	return face


while True:
	_, frame = camera.read()

	try:
		face = crop_face(frame)
		mask, without_mask = model.predict(face)[0]
	except Exception as e:
		print(e)
		mask, without_mask = 0, 0

	print(mask, without_mask)

	if mask > without_mask:
		text = "Mask: {:.2f}".format(max(mask, without_mask)*100)
		color = (0, 255, 0)
	elif mask < without_mask:
		text = "No mask: {:.2f}".format(max(mask, without_mask)*100)
		color = (0, 0, 255)
	else:
		text = ""

	if len(text) > 0:
		frame = cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

	cv2.imshow("frame", frame)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break


cv2.destroyAllWindows()
camera.release()