import keras
import cv2
import numpy as np

np.set_printoptions(suppress=True)
model = keras.models.load_model("./model/keras_model.h5")
classes = [line.strip() for line in open("./model/labels.txt", "r").readlines()]

video = cv2.VideoCapture("./data/video3.mp4")

while True:
    ret, image = video.read()
    if not ret:
        break 
    
    rectangles = [
        (220, 660, 350, 860),  # Rectangle 1
        (350, 660, 480, 860),  # Rectangle 2
        (480, 660, 610, 860),  # Rectangle 3
        (630, 660, 760, 860),  # Rectangle 4
        (760, 660, 890, 860)   # Rectangle 5
    ]

    for idx, (x1, y1, x2, y2) in enumerate(rectangles):
        cv2.rectangle(image, (x1, y2), (x2, y1), (0, 255, 0) if x2 <= 610 else (255, 0, 0), 3)
        cropped_image = image[y1:y2, x1:x2]
        cropped_image = cv2.resize(cropped_image, (224, 224), interpolation=cv2.INTER_AREA)

        cv2.imshow(f"Processed Image {idx + 1}", cropped_image)

        image_to_predict = np.asarray(cropped_image, dtype=np.float32).reshape(1, 224, 224, 3)
        image_to_predict = (image_to_predict / 127.5) - 1

        prediction = model.predict(image_to_predict)
        index = np.argmax(prediction)
        class_name = classes[index]
        confidence_score = np.round(prediction[0][index] * 100, 2)

        text = f"{class_name}: {confidence_score}%"
        cv2.putText(image, text, (x1, y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Video", image)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()
