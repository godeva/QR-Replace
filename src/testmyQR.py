#!/usr/bin/env python3
import myqr
from PIL import Image
import qrcode
import mathutil
from sklearn.datasets.samples_generator import make_blobs

#load a basic image for processing. (we can only handle RGB images)
im = Image.open("../TestImages/basicQRcode.png")
im = im.convert("RGB")
im2 = Image.open("../TestImages/tiltedQRcode.jpg")

#test findQR
#print(myqr.findQR(im))

#test insertQR
#print(myqr.insertQR(im), bounds, data)

#test diffColors
a = (1, 2, 3)
b = (2, 3, 4)
print("testing diffColors with ", a," and ", b)
print(myqr.diffColors(a,b))#should yield 3

#test diffPoints
print("\ntesting diffPoints with ", im.getpixel((10,10))," and ", im.getpixel((100,10)))
print(myqr.diffPoints(im, (10, 10), (100, 10)))

print("\ntesting diffPoints with ", im2.getpixel((10,10))," and ", im2.getpixel((100,10)))
print(myqr.diffPoints(im2, (10, 10), (100, 10)))

#test kindaEquals
print("\ntesting kindaEquals(5,5)")
print(mathutil.kindaEquals(5,5))
print("testing kindaEquals(5,60)")
print(mathutil.kindaEquals(5,60))

#test  distance
a1 = (3,0)
b1 = (0,0)
print("\ntesting distance between (3,0) and (0,0))")
print(myqr.distance(a1,b1))#should yield three

#test getPixelClusters
print("\nfinding consecutive similarly colored pixels")
im3 = Image.open("../TestImages/TestClusters.png")
print(myqr.getPixelClusters(im3, (0, 15), (1,0)))

#test extrapolateParallelogram
p1 = (5,5)
p2 = (10,6)
p3 = (4,10)
p4 = (9,11)
print("\nextrapolate parallelogram given p1,p2,p3...")
print(myqr.extrapolateParallelogram(p1,p2,p3))
print("extrapolate parallelogram given p2,p4,p3...")
print(myqr.extrapolateParallelogram(p2,p4,p3))

#test warpImage
parallelogram = [(75,50),(150,60),(150,150), (50,150)]
parallelogram2 = [(250,250),(400,120),(641,300), (440,440)]
warped = myqr.warpImage(im2, im, parallelogram2)
print("\ntesting image warping...")
im.show()
warped.show()

data, labels = make_blobs(n_samples=20, centers=[[10,10],[50,10],[10,50]])
print(data.shape)
print(myqr.constructParallelograms(data))
