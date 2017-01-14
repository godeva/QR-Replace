#!/usr/bin/env python3
from PIL import Image
import qrcode
import itertools
'''
NOTE:
color-tuples are 3 element tuples structred as (R,G,B), 0-255 each

point-tuples are 2 element tuples structed as (x,y)
(note that this is consistent with pillows use of points)
vectors are equivalent to point-tuples, but with a different context

quadrilateral-tuples are 4 element tuples structured as (point-tuple,point-tuple,point-tuple,point-tuple)
'''

def addTuples(t1, t2):
	'''
	@params:
		t1 is a tuple
		t2 is a tuple
	Adds the contents of each tuple, element by element.
	EX: addTuples((1,2),(4,6)) -> (5,8)
	@jacob
	'''
	return piecewiseMap(t1, t2, lambda x,y: x+y)

def piecewiseMap(t1, t2, fn):
	'''
	@params:
		t1 is a tuple
		t2 is a tuple
		fn is a function taking two parameters, and returning a single value
	Maps corresponding params of t1 and t2 by index.
	Calls supplied function as fn(t1[i], t2[i]) for each i in len(tuples)
	Returns a tuple of min((len(t1), len(t2)))
	'''
	return tuple(fn(x,y) for x,y in zip(t1,t2))

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
		image is the PIL image to sample from
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
		delta = diffPoints(image, last_point, next_point)

		#Check if delta below thresh; if so, Continue
		if delta < threshold:
			cluster_size += 1
		else:
			#Else, add to ret vals
			ret_vals += [(cluster_start, cluster_size)]
			cluster_start = next_point
			cluster_size = 1

		last_point = next_point
		next_point = addTuples(last_point, direction)

	#Add last value to clusters
	ret_vals += [(cluster_start, cluster_size)]
	return ret_vals


def findQR(image):
	'''
	@params:
		image is the image that we'll be messing with
	Returns n quadrilateral-tuples where n is the number of QR codes in the image.
	'''
	clusters = getPixelClusters(image)
	pass #@todo(someone) finish this


def insertQR(image, bounds, data):
	'''
	@params:
		image is the image that we'll be messing with
		bounds is a quadrilateral-tuple specifying where to place the image
		data is what will be encoded in the QR code
	inserts a QR code into the image at the specified bounds
	the new qr code should fit the bounds and seem natural (like it was the original imge)
	'''
	pass #@todo(someone) implement this

def isInBounds(image, point):
	'''
	@params:
		image is the image that we'll be messing with
		point is a tuple-point that we are testing
	returns a boolean
		True if the point is inside the image
		False if the point is outside the image
	'''
	size = image.size
	p = point
	return p.x >= 0 and p.y >= 0 and p.x < size.width and p.y < size.height
	#return all([dim > loc for dim,loc in zip(size,point)]) #jacob wrote this hideous line of code and said fight me and its bad
	#return all([size[i] > point[i] for i in range(2)]) or min(point) =< 0

def distance(a, b):
	'''
	@params:
		a is a point-tuple
		b is another point-tuple
	returns a double representing distance between the two points
	'''
	return math.hypot(a.x - b.x, a.y - b.y)

def angleOf(vector):
	'''
	@params:
		vector is a vector-tuple
	returns a double representing the vectors clockwise rotation from the x axis
		values range from [0,2pi)
	'''
	at = atan(vector[1], vector[0])
	if at < 0:
		at += 2*math.pi
	return at

def clockwiseRotation(from_v, to_v):
	'''
	@params:
		from_v is a vector-tuple
		to_v is a vector-tuple
	returns a double representing the total rotation from vector from_v
		to the vector to_v. Value returned is in range [0,2pi).
		Used to determine which point is the "upper" clockwise leg of a triangle
	'''
	a = angleOf(from_v) - angleOf(to_v)
	if a < 0`:
		a += 2 * math.pi
	return a

def extrapolateParallelogramJ(a, b, c):
	'''
	@params:
		a is one of the detected clusters in the image
		b ditto
		c ditto
	returns a list of four points representing vertices of parallelogram
		in clockwise order. The new point is generated based on the previous 3.
	'''

	def deduceKnownCorner(a, b, c): #Get points as (corner, another, another)
		segs = ((a,b), (b,c), (a,c))
		sorted_distance = sorted(segs, key=lambda seg: distance(seg[0], seg[1]))
		longest_seg = sorted_distance[2]
		return sorted((a,b,c), key=lambda p: p in longest_seg)

	def orderByRotation(a, b, c): #Orders points of triangle clockwise. First point is anchor. Tuple of tuple-point
		cp = deduceKnownCorner(a,b,c)
		corner = cp[0]
		a = cp[1]
		b = cp[2]

		#Get vectors from corner to each leg
		v_corner_a = piecewiseMap(corner, a, lambda x,y: y - x)
		v_corner_b = piecewiseMap(corner, b, lambda x,y: y - x)

		#Find which comes vector 'first', clockwise from x axis
		#Determined by which has lower clockwise angle
		rab = clockwiseRotation(v_corner_a, v_corner_b)
		rba = clockwiseRotation(v_corner_b, v_corner_a)

		if rab < rba:
			return (corner, a, b)
		else:
			return (corner, b, a)

	def genThirdPoint(ordered_points): #Takes result of orderByRotation, returns final point
		#Just generate a parallelogram u dingaling
		corner = ordered_points[0]
		leg1 = ordered_points[1]
		leg2 = ordered_points[2]
		vec_corner_leg1 = piecewiseMap(corner, leg1, lambda x,y: y - x)

		#Add this vec to leg2 to get final point of pgram.
		return addTuples(leg2, vec_corner_leg1)

	op = orderByRotation(a,b,c)
	np = genThirdPoint(op)
	return (op[0], op[1], np, op[2])

def extrapolateParallelogram(a, b, c):
	'''
	@params:
		a is one point-tuple in the parallelogram
		b is another point-tuple
		c is the third point-tuple
	returns a sequence of four points representing vertices of parallelogram
		formed by the points, that most closely resembles a square
		i.e. ((xa,ya), (xb,yb), (xc,yc), (xd,yd))
		points are returned in sorted order(first by x then y)
	'''
	dist = [distance(a,b), distance(b,c), distance(a,c)]
	maxIndex = dist.index(max(dist))

	#determine which side is longest, so we can find which direction to go
	if maxIndex == 0:
		point1, point2, point3 = a,b,c
	if maxIndex == 1:
		point1, point2, point3 = b,c,a
	if maxIndex == 2:
		point1, point2, point3 = a,c,b

	#find all possile new points from vector addition, and see which two are equal
	p1 = addTuples(tuple(x-y for x,y in zip(point1, point3)), point2)
	p2 = addTuples(tuple(y-x for x,y in zip(point1, point3)), point2)
	p3 = addTuples(tuple(x-y for x,y in zip(point2, point3)), point1)
	p4 = addTuples(tuple(y-x for x,y in zip(point2, point3)), point1)

	if p1 == p4:
		point4 = p1
	if p1 == p3:
		point4 = p1
	if p2 == p4:
		point4 = p2
	if p2 == p3:
		point4 = p2

	parallelogram = (point1, point2, point3, point4)

	return sorted(parallelogram)
