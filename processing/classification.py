import urllib.request
import cv2
import numpy as np
import string
import tensorflow as tf
import urllib
import pyrebase
import re
import time

def firebase_config():
    config = {
        "apiKey": "AIzaSyBhFKQ73tsHA7ZFQnel2D7tuUkHNHie1ug",
        "authDomain": "kwhmeter-d9fda.firebaseapp.com",
        "databaseURL": "https://kwhmeter-d9fda-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "kwhmeter-d9fda",
        "storageBucket": "kwhmeter-d9fda.appspot.com",
        "messagingSenderId": "539756566253",
        "appId": "1:539756566253:web:c18ecd52b0a7bc82b8dee4",
        "measurementId": "G-JL73R0L5BT"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase.database()

alphabet = string.digits + string.ascii_lowercase + '.'
blank_index = len(alphabet)

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

def format_text(text):
    filtered_text = re.sub(r'[^0-9.]', '', text)
    if len(filtered_text) > 2:
        return filtered_text[:-2] + '.' + filtered_text[-2:]
    return filtered_text

def main():
    db = firebase_config()
    type_value = db.child("type").get().val() or 'kwh'
        
    video_path = 'http://192.168.65.231/cam-hi.jpg'
    
    last_push_time = 0
    push_interval = 5
    last_text = None
    
    model_path = './model/model_float16.tflite'

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    while True:
        try:
            img_resp = urllib.request.urlopen(video_path)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, cv2.IMREAD_COLOR)
            
            if frame is None:
                print("Failed to fetch frame from ESP32-CAM")
                break
            
            result = predict(frame, interpreter)
            text = "".join(alphabet[index] for index in result[0] if index not in [blank_index, -1])
            
            if len(text) >= 3:
                cv2.putText(frame, f'Extracted text: {text}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if type_value == 'kwh':
                    formatted_text = float(format_text(text))
                else:
                    formatted_text = text
                print(f"Formatted Text: {formatted_text}")
                try:
                    numeric_value = float(formatted_text)
                    current_time = time.time()
                    if (current_time - last_push_time > push_interval) and (formatted_text != last_text):
                        db.child('data').child('balances').set(numeric_value)
                        last_push_time = current_time
                        last_text = formatted_text
                        print(f"Updated Firebase with: {numeric_value}")
                except ValueError:
                    print(f"Conversion error: '{formatted_text}' is not a valid float")
                
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            
        except Exception as e:
            print(f"Error fetching frame: {e}")
            break
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
