#!/usr/bin/env python3
import myqr
from PIL import Image
import qrcode
import mathutil
from sklearn.datasets.samples_generator import make_blobs
from mathobjects import *

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
#print("\ntesting diffPoints with ", im.getpixel((10,10))," and ", im.getpixel((100,10)))
print(myqr.diffPoints(im, Point(10, 10), Point(100, 10)))

print("\ntesting diffPoints with ", im2.getpixel((10,10))," and ", im2.getpixel((100,10)))
print(myqr.diffPoints(im2, Point(10, 10), Point(100, 10)))

#test kindaEquals
print("\ntesting kindaEquals(5,5)")
print(mathutil.kindaEquals(5,5))
print("testing kindaEquals(5,60)")
print(mathutil.kindaEquals(5,60))

#test  distance
a1 = Point(3,0)
b1 = Point(0,0)
print("\ntesting distance between (3,0) and (0,0))")
print(a1.distance(b1))#should yield three

#test getPixelClusters
print("\nfinding consecutive similarly colored pixels")
im3 = Image.open("../TestImages/TestClusters.png")
im3 = im3.convert("RGB")
print(myqr.getColorGroups(im3, Point(0,0), Point(1,0)))

#test extrapolateParallelogram
p1 = Point(5,5)
p2 = Point(10,6)
p3 = Point(4,10)
p4 = Point(9,11)
print("\nextrapolate parallelogram given p1,p2,p3...")
print(myqr.extrapolateParallelogram(p1,p2,p3))
print("extrapolate parallelogram given p2,p4,p3...")
print(myqr.extrapolateParallelogram(p2,p4,p3))

#test warpImage
parallelogram = [Point(75,50),Point(150,60),Point(150,150), Point(50,150)]
parallelogram2 = [Point(277,288),Point(389,111),Point(571,230), Point(458,403)]
im4 = Image.open("../TestImages/cropped-qr.jpg")
warped = myqr.warpImage(im2, im4, parallelogram2)
print("\ntesting image warping...")
i = Image.open("../TestImages/tiltedQRcode.jpg")
i.show()
warped.show()

data, labels = make_blobs(n_samples=20, centers=[[10,10],[50,10],[10,50]])
print(data.shape)
print(mathutil.constructParallelograms(data))

#test expandParallelogram
print(mathutil.expandParallelogram(parallelogram, 4))
print(myqr.getMassQRClusters(im, 1))

print(myqr.scanImage2(im))
