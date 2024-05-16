import numpy as np
import cv2

import ocraux as ocraux
import brightcontras as brco
import binarization as bi

def configImagen(img):
    fotoDif = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    c_t = ocraux.elegirCoord(fotoDif)
    N = int(input("\n --> Insert number of digits >> "))
    
    imROI = ocraux.cutROI(fotoDif, c_t)
    
    bc = brco.BrightContr(imROI)
    cv2.waitKey()
    cv2.destroyAllWindows()
    alpha, beta = bc.alpha, bc.beta

    binar = bi.Binarizador(bc.transformada)
    cv2.waitKey()
    cv2.destroyAllWindows()
    size, offset = binar.size, binar.offset
    
    digitos = ocraux.setupROI(bc.transformada, N, c_t)

    num_base = ocraux.CargarBaseReescalar("./img/numeros_base.png", digitos, mostrar=True)
    setup = {"c_t": c_t,
            "N": N,
            "num_base": num_base,
            "alpha": alpha,
            "beta": beta,
            "size": size,
            "offset": offset}
    return setup

def configCamara(cap):
    print("--- Capture 1.0 -- Seven Segment Optical Character Recognition ---")
    print("\n INFO: Jika muncul gambar, tutup dengan menekan 'q' untuk melanjutkan program.")
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    print("[*] Objeto de cámara creado")

    print("\n --> Pasang layar mati..")
    ocraux.mostrarWebcam(cap)
    ret, fondo = cap.read()
    imgApagado = ocraux.convGris(fondo)

    print("\n --> Nyalakan tampilan dan tekan 'q' untuk mendapatkan gambar pertama...")
    ocraux.mostrarWebcam(cap)

    ret, imagen = cap.read()
    imgPrendido = ocraux.convGris(imagen)
    print("Foto dengan angka yang diambil.")
        
    fotoDif = ocraux.mat2img(np.abs(imgApagado - imgPrendido))
    
    c_t = ocraux.elegirCoord(fotoDif)
    N = int(input("\n --> Masukkan jumlah digit >> "))
    
    digitos = ocraux.setupROI(fotoDif, N, c_t)
    
    ocraux.binarizar(digitos, mostrar=True)
    num_base = ocraux.CargarBaseReescalar("./img/numeros_base.png", digitos, mostrar=True)

    return imgApagado, c_t, N, num_base

def adquirirImagen(cap, imgApagado):
    for i in range(5):
        ret, imagen = cap.read()
    if not(ret):
        print("Error...")
    imgPrendido = ocraux.convGris(imagen)
    
    fotoDif = ocraux.mat2img(np.abs(imgApagado - imgPrendido))
    return fotoDif

def adquirirNumero(fotoDif, set_up, ver=False):

    imROI = ocraux.cutROI(fotoDif, set_up["c_t"], mostrar=ver)
    
    imROIbc = np.clip(set_up["alpha"]* imROI.astype('float32') + set_up["beta"], 0, 255)
    imROIbc = imROIbc.astype('uint8')
    
    imROI_bin = ocraux.binarizarUnaImagen(imROIbc, size=set_up["size"], C=set_up["offset"], mostrar=ver)
    digitos_bin = ocraux.setupROI(imROI_bin, set_up["N"], set_up["c_t"], mostrar=ver)

    res_posibles, confianzas = ocraux.comparar(digitos_bin, set_up["num_base"], mostrar=ver)
    return res_posibles, confianzas