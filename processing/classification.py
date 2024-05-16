import urllib.request
import cv2
import numpy as np
import string
import tensorflow as tf
import os
import urllib
import sys

alphabet = string.digits + string.ascii_lowercase + '.'
blank_index = len(alphabet)

x, y, w, h = 10, 670, 800, 650

def prepare_input(image):
    input_data = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    input_data = cv2.resize(input_data, (200, 31))
    input_data = input_data[np.newaxis]
    input_data = np.expand_dims(input_data, 3)
    input_data = input_data.astype('float32') / 255
    return input_data

def predict(image, interpreter):
    input_data = prepare_input(image)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    return output

def main():
    video_path = './data/kwh12.mp4'
    # video_path = 'http://192.168.1.61/cam-hi.jpg'
    
    model_path = './model/model_float16.tflite'
    if not os.path.isfile(video_path):
        print(f'{video_path} does not exist')
        sys.exit()

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # cap = cv2.VideoCapture(video_path)

    while True:
        try:
            img_resp = urllib.request.urlopen(video_path)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)
            # ret, frame = cap.read()
            
            if frame is None:
                print("Failed to fetch frame from ESP32-CAM")
                break
            
            roi = frame[y:y+h, x:x+w]

            result = predict(roi, interpreter)
            text = "".join(alphabet[index] for index in result[0] if index not in [blank_index, -1])
            
            cv2.putText(frame, f'Extracted text: {text}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Video', frame)
            cv2.imshow('ROI', roi)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            
        except Exception as e:
            print(f"Error fetching frame: {e}")
            break
        
    # cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
