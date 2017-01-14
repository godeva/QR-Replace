#!/usr/bin/env python3
import myqr
from PIL import Image
import qrcode

#load a basic image for processing.
im = Image.open("../TestImages/basicQRcode.png")

#test findQR
print(myqr.findQR(im))

#test insertQR
#print(myqr.insertQR(im), bounds, data)

#test diffColors, should yield 3
a = [1, 2, 3]
b = [2, 3, 4]
print(myqr.diffColors(a,b))
