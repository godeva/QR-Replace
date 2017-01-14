#!/usr/bin/env python3
from PIL import Image
import qrcode

'''
NOTE:
color-tuples are 3 element tuples structred as (R,G,B), 0-255 each
point-tuples are 2 element tuples structed as (x,y)
(note that this is consistent with pillows use of points)
vectors are equivalent to point-tuples, but with a different context
'''

def addTuples(t1, t2):
	'''
	@params:
		t1 is a tuple
		t2 is a tuple
	Adds the contents of each tuple, element by element.
	EX: addTuples((1,2),(4,6)) -> (5,8)
	No idea what happens if different sizes
	@jacob
	'''
	return tuple(x+y for x,y in zip(t1,t2))

def diffColors(a, b):
    '''
    @params:
        a is a color-tuple
        b is a color-tuple

    Yield an integer value representing total difference among color values.
    Difference is computed for each R, G, B of color
    Ranges from 0 (same color) to 765 (max difference)
    '''
    return sum(abs(x - y) for x,y in zip(a,b))


def diffPoints(image, p1, p2):
    '''
    @params:
        image is the PIL immage to sample from
        p1 is a point-tuple
        p2 is a point-tuple

    Delegate call to diffColors on two points in an image
    '''
    a = image.getpixel(p1)
    b = image.getpixel(p2)
    return diffColors(a,b)

def getPixelClusters(image, start, direction):
    '''
    @params:
        image is the PIL image to sample from
        start is a point-tuple defining where to begin scanning clusters
        direction is a vector defining direction to travel

    Scan over an image from a starting point until end of image is reached.
    Scan results are returned as a list of tuples containing the start point of
    the cluster, and the length of that cluster.
    EX:
    [((5,0), 15), ((5,15), 7), ...]
       ^--point-tuple      ^--length of cluster

    direction as a vector allows this function to be used for vertical, horizontal,
    diagonal, or any angle of traversal, at varying levels of precision.
    '''
    ret_vals = [] #Create list to add clusters to
    last_point = start
	next_point = addTuples(last_point, direction)

	#Track current cluster
	cluster_start = last_point
	cluster_size = 1

    threshold = 50
    #Continue scanning until curr_point is outside of image
    while isInBounds(image, next_point):
		delta = diffPoints(next_point)

		#Check if delta below thresh; if so, Continue
		if delta < thresh:
			cluster_size += 1
		else:
			#Else, add to ret vals
			ret_vals.push_back((cluster_start, cluster_size))
			cluster_start = next_point
			cluster_size = 1

		last_point = next_point
		next_point = addTuples(last_point, direction)

	#Add last value to clusters
	ret_vals.push_back((cluster_start, cluster_size))
	return ret_vals


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
    pass #@todo(someone) implement this

def isInbounds(image, point):
    '''
    @params:
        image is the image that we'll be messing with
        point is a tuple-point that might
    returns a boolean
        true if the point is inside the image
        flase if the point is outside the image
    '''
    size = image.size
    #return all([dim > loc for dim,loc in zip(size,point)]) jacob wrote this hideous line of code and said fight me and its bad
    return all([size[i] > point[i] for i in range(2)]) or min(point) =< 0