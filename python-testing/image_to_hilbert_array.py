from hilbertcurve.hilbertcurve import HilbertCurve
from PIL import Image
import math
import os
import matplotlib.pyplot as plt
import numpy as np

class HSVPixel:
    hue: int
    saturation: int
    value: int

    def __init__(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value

MAXORDER = 10

hilbertPoints = []
computedOrder = -1

def imageToHilbertArray(img: Image, pxarray: list):
    global MAXORDER, hilbertPoints, computedOrder

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

    width, height = img.size
    newszexp = min ( max ( max ( getGeqPowerOf2(width), getGeqPowerOf2(height) ), 1 ), MAXORDER )
    newsz = 2 ** newszexp

    img = img.resize((newsz, newsz))
    hsvimg = img.convert("HSV")

    if newszexp != computedOrder:
        hilbertPoints.clear()
        hilbertCurve = HilbertCurve(newszexp, 2, 0)
        hilbertPoints = hilbertCurve.points_from_distances(list(range(newsz * newsz)))
        hilbertPoints = [[x, newsz-1 - y] for [x, y] in hilbertPoints]
        computedOrder = newszexp

    pxarray.clear()

    for point in hilbertPoints:
        px = hsvimg.getpixel((point[0], point[1]))
        pxarray.append(HSVPixel(px[0], px[1], px[2]))

pxarray = []
mypath = os.path.dirname(__file__)
print(mypath)

with Image.open(mypath + r"\blackandwhite2.png") as img:
    imageToHilbertArray(img, pxarray)


