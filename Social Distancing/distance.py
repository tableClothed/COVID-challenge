import cv2
import numpy as np
import os
import imutils 

MIN_CONF = 0.3
THRESH = 0.3
MIN_DISTANCE = 50 # in pixels

LABELS = []
with open("yolo/coco.names", "r") as f:
    LABELS = [line.strip() for line in f.readlines()]

net = cv2.dnn.readNet("yolo/yolov3.weights", "yolo/yolov3.cfg")

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

camera = cv2.VideoCapture(0)
writer = None


# -----------------------------
#           FUNCTION
# -----------------------------


def detect_people(frame, net, ln, personId=0):
    h, w = frame.shape[:2]
    results = []
    
    blob = cv2.dnn.bloblFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_out = net.forward()
    
    boxes = []
    centroids = []
    probabilities = []
    
    for output in layer_out:
        for detection in output:
            scores = detection[:5]
            class_id = np.argmax(scores)
            probab = scores[class_id]
            
#             if the object is a person and min confidence is met
            if class_id == personId and probab > MIN_CONF:
                # scale cunding box coords
                box = detection[0:4] * np.array([w, h, w, h])
                
                (cX, cY, width, height) = box.astype("int")
                
                x = int(cX - (width/2))
                y = int(xY - (height/2))
                
                boxes.append([x, y, int(width), int(height)])
                controids.append((cX, cY))
                probabilities.append(float(probab))
                
        ids = cv2.dnn.NMSBoxes(boxes, probabilities, MIN_CONF, THRESH)
        
        if len(ids) > 0:
            for i in ids.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                
                r = (probabilities[i], (x, y, x+w, y_h), centroids[i])
                results.append(r)
        return results 


# -----------------------------
#            MAIN
# -----------------------------



while True:
    ret, frame = camera.read()
    
    if not ret: break
        
    frame = imutils.resize(frame, width=700)
    