#!/usr/bin/env python3
import myqr
from PIL import Image
import qrcode

#load a basic image for processing. (we can only handle RGB images)
im = Image.open("../TestImages/basicQRcode.png")

im = im.convert("RGB")
im2 = Image.open("../TestImages/tiltedQRcode.jpg")

#test findQR
print(myqr.findQR(im))

#test insertQR
#print(myqr.insertQR(im), bounds, data)

#test diffColors
a = (1, 2, 3)
b = (2, 3, 4)
print(myqr.diffColors(a,b))#should yield 3

#test diffPoints
print(myqr.diffPoints(im, (10, 10), (100, 10)))
print(myqr.diffPoints(im2, (10, 10), (100, 10)))

#test  distance
a1 = (3,0)
b1 = (0,0)
print(myqr.distance(a1,b1))#should yield three

#test getPixelClusters
im = Image.open("../TestImages/TestClusters.png")
print(myqr.getPixelClusters(im, (0, 15), (1,0)))

#test extrapolateParallelogram
p1 = (5,5)
p2 = (10,6)
p3 = (4,10)
p4 = (9,11)
print(myqr.extrapolateParallelogram(p1,p2,p3))
print(myqr.extrapolateParallelogram(p2,p4,p3))
