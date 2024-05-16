from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2
import tkinter as tk
from tkinter import Scale

DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
    (1, 0, 1, 1, 1, 1, 0): 2,
    (1, 0, 1, 1, 0, 1, 1): 3,
    (0, 1, 1, 1, 0, 1, 0): 4,
    (1, 1, 0, 1, 0, 1, 1): 5,
    (1, 1, 0, 1, 1, 1, 1): 6,
    (1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

# Tkinter window setup
def update_values(*args):
    global low_threshold, high_threshold
    low_threshold = low_slider.get()
    high_threshold = high_slider.get()

root = tk.Tk()
root.title("Canny Edge Detection Settings")

low_slider = Scale(root, from_=0, to=255, label="Low Threshold", orient='horizontal', command=update_values)
low_slider.set(0)
low_slider.pack()

high_slider = Scale(root, from_=0, to=255, label="High Threshold", orient='horizontal', command=update_values)
high_slider.set(220)
high_slider.pack()

video = cv2.VideoCapture('./data/kwh13.mp4')

x, w = 0, 430
y, h = 110, 220
low_threshold = 10
high_threshold = 220

while True:
    ret, image = video.read()
    if not ret:
        break

    image = imutils.resize(image, height=500)
    image = image[y:y+h, x:x+w]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(blurred, 120, 200, 255)
    
    cv2.imshow("Video", image)
    cv2.imshow("Edged", edged)

    # thresh = cv2.threshold(gray, low_slider.get(), high_slider.get(), cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("Thresh", thresh)

    if cv2.waitKey(1) == 27:
        break

    root.update_idletasks()
    root.update()

video.release()
cv2.destroyAllWindows()
root.destroy()
