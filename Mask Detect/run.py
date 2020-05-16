import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import dlib
from PIL import Image
import imutils
from imutils import face_utils
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

model = load_model("models/MobileNetV2.h5")

camera = cv2.VideoCapture(0)
face_detector = dlib.get_frontal_face_detector()

# p = "data/shape_predictor_68_face_landmarks.dat"
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(p)

def crop_face(image):

    detected_face = face_detector(image, 1)
    face_frames = [(x.left(), x.top(),
                    x.right(), x.bottom()) for x in detected_face]

    return face_frames


while True:
    _, frame = camera.read()

    # w, h = frame.shape[:2]

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # rects = detector(gray, 0)
    # for rect in rects:
        # shape = predictor(gray, rect)
        # shape = face_utils.shape_to_np(shape)
        # shape =

        # face_x = shape[0][0]
        # face_y = shape[16][0]
    face_rect = crop_face(frame)
    print(face_rect)
    face = Image.fromarray(frame).crop(face_rect)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    face = np.expand_dims(face, axis=0)


    mask, without_mask = model.predict(face)[0]

    text = "Mask" if mask > without_mask else "No mask"
    color = (0, 255, 0) if text == "Mask" else (0, 0, 255)

    text += f": {max(mask, without_mask)*100}%"

    frame = cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 20, color, 2)

    cv2.imshow(frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
camera.release()