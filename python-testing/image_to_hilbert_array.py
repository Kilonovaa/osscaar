from hilbertcurve.hilbertcurve import HilbertCurve
from PIL import Image
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2

class HSVPixel:
    hue: int         # 0-179
    saturation: int  # 0-255
    value: int       # 0-255

    def __init__(self, hue: int, saturation: int, value: int):
        self.hue = hue
        self.saturation = saturation
        self.value = value

MAXORDER = 8

hilbertPoints = []
computedOrder = -1

def imageToHilbertArray(img):
    global MAXORDER, hilbertPoints, computedOrder

    if not isinstance(img, np.ndarray):
        img = np.array(img)

    def getGeqPowerOf2(nr: int):
        if nr <= 1:
            return 0
        aux = (int(math.log2(nr)))
        val = 2 ** aux
        while val < nr:
            aux += 1
            val *= 2
        while val // 2 >= nr:
            aux -= 1
            val //= 2
        return aux

    height, width, _ = img.shape
    newSzExp = min ( max ( max ( getGeqPowerOf2(width), getGeqPowerOf2(height) ), 1 ), MAXORDER )
    newSz = 2 ** newSzExp

    cvImage = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    cvImage = cv2.resize(cvImage, (newSz, newSz))

    if newSzExp != computedOrder:
        hilbertPoints.clear()
        hilbertCurve = HilbertCurve(newSzExp, 2, 0)
        hilbertPoints = hilbertCurve.points_from_distances(list(range(newSz * newSz)))
        computedOrder = newSzExp

    pxArray = []

    for point in hilbertPoints:
        px = cvImage[point[0]][point[1]]
        pxArray.append(HSVPixel(px[0], px[1], px[2]))
    
    return pxArray


# pxarray = []
# mypath = os.path.dirname(__file__)
# print(mypath)

# with Image.open(mypath + r"\blackandwhite2.png") as img:
#     imageToHilbertArray(np.array(img), pxarray)
#     for pixel in pxarray:
#         print(pixel.value)
#     # xPoints = np.array([x for [x, y] in hilbertPoints])
#     # yPoints = np.array([y for [x, y] in hilbertPoints])
#     # plt.plot(xPoints, yPoints)
#     # plt.show()

