import cv2
import pytesseract
from pytesseract import Output

cap = cv2.VideoCapture('./data/video1.mp4')
width = 480
ratio = width / cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * ratio)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    x, y, w, h = 95, 260, 400, 150
    roi = resized[y:y+h, x:x+w]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
    edged = cv2.Canny(gray, 200, 100, apertureSize=3)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    digit_contours = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 20 and h > 20:
            roi_cnt = edged[y:y+h, x:x+w]
            text = pytesseract.image_to_data(roi_cnt, config='--psm 6')
            print(text)
            cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Video', resized)
    cv2.imshow('Threshold', thresh) 
    cv2.imshow('Edged', edged)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows() 