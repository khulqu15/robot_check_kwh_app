import matplotlib.pyplot as plt
import numpy as np
import cv2

import ocr

plt.close('all')

setup = ocr.configImagen("./data/14.png")

res = np.array([])
con = np.array([])

for n in range(19,22):
    fotoDif = cv2.imread("./tanda1/%i.png"%n, cv2.IMREAD_GRAYSCALE)
    
    res_posibles, confianzas = ocr.adquirirNumero(fotoDif, setup, ver=True)

    res = np.append(res, res_posibles[:,-1])
    con = np.append(con, (confianzas[:,-1]*100).astype("int32"))
    print("Possible results: digits in rows, decreasing order")
    print(*res_posibles[:,-3:].transpose()[::-1], sep='\n')
    print("Confidence (distance to next option)")
    print(*((confianzas[:,-3:]*100).astype("int32")).transpose()[::-1], sep='\n')
    print("")
    
    cv2.destroyAllWindows()
    plt.close('all')