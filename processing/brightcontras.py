import cv2

class BrightContr:
    def __init__(self, image):
        import numpy as np
        self.imagen = image
        self.transformada = image
        self.alpha = 1
        self.beta = 0
        self.title_window = 'Ventana Brightness and Contrast'
        cv2.namedWindow(self.title_window, cv2.WINDOW_KEEPRATIO)
        
        cv2.createTrackbar('Alpha', self.title_window, 50, 100, self.on_trackbar_alpha)
        cv2.createTrackbar('Beta', self.title_window, 50, 100, self.on_trackbar_beta)
        self.update()

    def on_trackbar_alpha(self, val):
        import numpy as np
        self.alpha = np.interp(val, [0,50,100], [0,1,10]) # Map to valid interval
        self.update()

    def on_trackbar_beta(self, val):
        import numpy as np
        self.beta = np.interp(val, [0,100], [-255,255])  # Map to valid interval
        self.update()

    def update(self):
        import numpy as np
                
        self.transformada = np.clip(self.alpha*self.imagen.astype('float32') + self.beta, 0, 255).astype('uint8')

        cv2.imshow(self.title_window, self.transformada)
