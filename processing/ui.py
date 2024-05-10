import cv2
import pytesseract
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

def preprocess_image(img, blur_size, dilate_iter, erode_iter):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (blur_size, blur_size), 0)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    kernel = np.ones((1, 1), np.uint8)
    img_dilate = cv2.dilate(img_thresh, kernel, iterations=dilate_iter)
    img_erode = cv2.erode(img_dilate, kernel, iterations=erode_iter)
    return img_erode

def update_processing(*args):
    try:
        blur_size = int(blur_scale.get())
        dilate_iter = int(dilate_scale.get())
        erode_iter = int(erode_scale.get())
        psm = psm_choice.get()
        oem = oem_choice.get()
        
        config = f'--oem {oem} --psm {psm} -c tessedit_char_whitelist=0123456789kWh'
        processed_img = preprocess_image(img, blur_size * 2 + 1, dilate_iter, erode_iter)
        x_roi, y_roi, w_roi, h_roi = 95, 260, 470, 170 # Image 1 Configuration
        # x_roi, y_roi, w_roi, h_roi = 110, 350, 400, 115 # Image 2 Configuration
        processed_img = processed_img[y_roi:y_roi+h_roi, x_roi:x_roi+w_roi]
        text = pytesseract.image_to_string(processed_img, config=config)
        image_display = Image.fromarray(processed_img)
        photo = ImageTk.PhotoImage(image=image_display)
        
        label_image.config(image=photo)
        label_image.image = photo
        label_text.config(text=f"Detected Text: {text}")
    except Exception as e:
        label_text.config(text=str(e))

# Load the image
image_path = './data/image1.png'
img = cv2.imread(image_path)

# Tkinter setup
root = Tk()
root.title("OCR Parameter Tuner")

# Creating sliders for parameters
blur_scale = Scale(root, from_=0, to_=20, orient=HORIZONTAL, label="Blur Size", command=update_processing)
blur_scale.set(1)
blur_scale.pack(fill=X)

dilate_scale = Scale(root, from_=0, to_=20, orient=HORIZONTAL, label="Dilate Iterations", command=update_processing)
dilate_scale.set(1)
dilate_scale.pack(fill=X)

erode_scale = Scale(root, from_=0, to_=20, orient=HORIZONTAL, label="Erode Iterations", command=update_processing)
erode_scale.set(2)
erode_scale.pack(fill=X)

# Dropdown for PSM and OEM
psm_choice = StringVar(root)
oem_choice = StringVar(root)
psm_choice.set('6')  # default value
oem_choice.set('3')  # default value

psm_dropdown = ttk.Combobox(root, textvariable=psm_choice, values=[str(i) for i in range(14)], state="readonly")
psm_dropdown.pack(fill=X)
oem_dropdown = ttk.Combobox(root, textvariable=oem_choice, values=[str(i) for i in range(4)], state="readonly")
oem_dropdown.pack(fill=X)

# Image display label
label_image = Label(root)
label_image.pack()

# OCR Text display label
label_text = Label(root, text="Detected Text: ", justify=LEFT)
label_text.pack(fill=X)

root.mainloop()
