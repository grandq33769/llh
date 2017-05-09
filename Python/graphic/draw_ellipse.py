'''Demo for drawing ellipse on jpg'''
import os
from PIL import Image, ImageDraw

BASE_URL = os.path.dirname(__file__)

IMG = Image.open(BASE_URL + '/mini.jpg')

X, Y = IMG.size
EX, EY = 30, 60  # Size of Bounding BoX for ellipse

BBOX = (X / 2 - EX / 2, Y / 2 - EY / 2, X / 2 + EX / 2, Y / 2 + EY / 2)
DRAW = ImageDraw.Draw(IMG)
DRAW.ellipse(BBOX, fill=128)
del DRAW

IMG.save("output.png")
IMG.show()
