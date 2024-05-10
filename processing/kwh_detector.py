import cv2
import numpy as np

# Load pre-trained EAST text detector
net = cv2.dnn.readNet('./frozen_east_text_detection.pb')

# Setup video capture
cap = cv2.VideoCapture('./data/video1.mp4')
width = 480
ratio = width / cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * ratio)

# Set up parameters for text detection
(confThreshold, nmsThreshold) = (0.5, 0.4)
layerNames = ["feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    x, y, w, h = 95, 260, 400, 150
    roi = resized[y:y+h, x:x+w]
    
    # Convert to blob for EAST detector
    blob = cv2.dnn.blobFromImage(roi, 1.0, (w, h), (123.68, 116.78, 103.94), True, False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    
    # Decode the predictions
    (rects, confidences) = ([], [])
    for i in range(geometry.shape[2]):
        for j in range(geometry.shape[3]):
            if scores[0][0][i][j] < confThreshold:
                continue
            
            offsetX, offsetY = (j * 4.0, i * 4.0)
            
            angle = geometry[0][4][i][j]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = geometry[0][0][i][j] + geometry[0][2][i][j]
            w = geometry[0][1][i][j] + geometry[0][3][i][j]
            
            endX = int(offsetX + (cos * geometry[0][1][i][j]) + (sin * geometry[0][2][i][j]))
            endY = int(offsetY - (sin * geometry[0][1][i][j]) + (cos * geometry[0][2][i][j]))
            startX = int(endX - w)
            startY = int(endY - h)
            
            rects.append((startX, startY, endX, endY))
            confidences.append(scores[0][0][i][j])
    
    # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(rects, confidences, confThreshold, nmsThreshold)
    for i in indices:
        (startX, startY, endX, endY) = rects[i[0]]
        cv2.rectangle(roi, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Display the results
    cv2.imshow('Video', resized)
    cv2.imshow('Text Detection', roi)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
