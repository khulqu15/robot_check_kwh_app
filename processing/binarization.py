import cv2

class Binarizador:
    def __init__(self,imagen):
        self.imagen = imagen
        default_size = imagen.shape[0]%2 - 1 + imagen.shape[0]
        print(default_size)
        self.size = default_size
        self.offset = 0
        self.title_window = 'Ventana'
        cv2.namedWindow(self.title_window, cv2.WINDOW_KEEPRATIO)
        
        cv2.createTrackbar('Size', self.title_window, self.size, default_size, self.on_trackbar_size)
        cv2.createTrackbar('Offset', self.title_window, self.offset, 20, self.on_trackbar_offset)
        self.update()

    def on_trackbar_size(self, val):
        self.size = (1 - val%2) + val + 2 # Para que siempre sea impar y mayor a 2
        self.update()

    def on_trackbar_offset(self, val):
        self.offset = val
        self.update()

    def update(self):
        print("Size\t %i \t Offset \t %i \n"%(self.size, self.offset))
        binarizada = cv2.adaptiveThreshold(self.imagen, 255,
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, self.size, self.offset)
        cv2.imshow(self.title_window, binarizada)
