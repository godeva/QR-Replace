#!/usr/bin/env python3
from __future__ import print_function
from PIL import Image
import qrcode

def diffColors(a, b):
	'''
	@params:
		a is a color-tuple
		b is a color-tuple

	Yield an integer value representing total difference among color values.
	Difference is computed for each R, G, B of color
	Ranges from 0 (same color) to 765 (max difference)
	'''
	diff = 0
	for x,y in zip(a,b):
		diff += abs(x - y)

	return diff




def findQR(image):
	'''
	@params:
		image is the image that we'll be messing with
	Scan a vertical line over the image and try to find the 1113111 patterns of white/black
	white is anything that's pretty white (find a way to determine that, probably with more machine learning)
	black is anything that's not white (so if it's a strong blue,red,green, etc. that counts as black)
	'''
	pass #@todo(someone) implement this


def insertQR(image, bounds, data):
	'''
	@params:
		image is the image that we'll be messing with
		bounds is where we're going to put the QR code
		data is what will be encoded in the QR code (we'll be generating the QR code to insert inside here)
	inserts a QR code into the image at the specified bounds
	the new qr code should fit the bounds and seem natural (like it was the original imge)
	'''

im = Image.open("basicQRcode.png")
im.show()

	pass #@todo(someone) implement this
