import cv2
import numpy as np
import os
import imutils
from scipy.spatial import distance as dist 

MIN_CONF = 0.3
THRESH = 0.3
MIN_DISTANCE = 50 # in pixels

LABELS = []
with open("YOLO_model/coco.names", "r") as f:
    LABELS = [line.strip() for line in f.readlines()]

net = cv2.dnn.readNet("YOLO_model/yolov3.weights", "YOLO_model/yolov3.cfg")

# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# ln = net.getLayerNames()
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

camera = cv2.VideoCapture("pedestrians.mp4")


# -----------------------------
#           FUNCTION
# -----------------------------


def detect_people(frame, net, ln, personId=0):
    h, w = frame.shape[:2]
    results = []
    
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_out = net.forward(ln)
    
    boxes = []
    centroids = []
    probabilities = []
    
    for output in layer_out:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            probab = scores[class_id]
            
            #if the object is a person and min confidence is met
            if class_id == personId and probab > MIN_CONF:
                # scale cunding box coords
                box = detection[0:4] * np.array([w, h, w, h])
                
                (cX, cY, width, height) = box.astype("int")
                
                x = int(cX - (width/2))
                y = int(cY - (height/2))
                
                boxes.append([x, y, int(width), int(height)])
                centroids.append((cX, cY))
                probabilities.append(float(probab))
                
    # non maxima suppression to suppress weak, overlapping boxes
    ids = cv2.dnn.NMSBoxes(boxes, probabilities, MIN_CONF, THRESH)
    
    if len(ids) > 0:
        for i in ids.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            r = (probabilities[i], (x, y, x+w, y+h), centroids[i])
            results.append(r)
    return results 


# -----------------------------
#            MAIN
# -----------------------------



while True:
    ret, frame = camera.read()
    
    if not ret: break
        
    frame = imutils.resize(frame, width=700)
    results = detect_people(frame, net, ln, personId=LABELS.index("person"))

    violate = set()

    if len(results) >= 2:
    	centroids = np.array([r[2] for r in results])
    	D = dist.cdist(centroids, centroids, metric="euclidean")

    	for i in range(0, D.shape[0]):
    		for j in range(i+1, D.shape[1]):
    				if D[i, j] < MIN_DISTANCE:
    					violate.add(i)
    					violate.add(j)

    for (i, (prob, bbox, centroid)) in enumerate(results):
    	(startX, startY, endX, endY) = bbox
    	(cX, cY) = centroid
    	color = (0, 255, 0)

    	# if index pair exists within the violation set, then update color
    	if i in violate:
    		color = (0, 0, 255)

    	cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    	cv2.circle(frame, (cX, cY), 5, color, 1)

    text = f"{len(violate)}"
    cv2.putText(frame, text, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
    	break

    