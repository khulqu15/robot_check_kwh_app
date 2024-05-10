import cv2
import pytesseract
import numpy as np

def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=2)
    return img

# Path to the image file
image_path = './data/image2.png'

# Preprocess the image
img = preprocess_image(image_path)

# Define the ROI coordinates directly on the preprocessed image
# x_roi, y_roi, w_roi, h_roi = 95, 260, 470, 170 # Image 1 Configuration
x_roi, y_roi, w_roi, h_roi = 110, 350, 400, 115 # Image 2 Configuration
roi = img[y_roi:y_roi+h_roi, x_roi:x_roi+w_roi]

# OCR configuration
config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789kWh'
detection_result = pytesseract.image_to_data(roi, config=config, output_type=pytesseract.Output.DICT)
detected_chars = []

for i, text in enumerate(detection_result['text']):
    if int(detection_result['conf'][i]) > 0:
        x, y, w, h = detection_result['left'][i], detection_result['top'][i], detection_result['width'][i], detection_result['height'][i]
        cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 255, 0), 2)
        detected_chars.append(text)
        

cv2.imshow('Detected Text', roi)
detected_text = pytesseract.image_to_string(roi, config=config)
print("Detected Text:", detected_text)
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     break

# Displaying the image
cv2.waitKey(0)
cv2.destroyAllWindows()
