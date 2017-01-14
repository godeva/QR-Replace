import math

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

def isInBounds(image, point):
	'''
	@params:
		image is the image that we'll be messing with
		point is a tuple-point that we are testing
	returns a boolean
		True if the point is inside the image
		False if the point is outside the image
	'''
	width, height = image.size
	p = point
	return p[0] >= 0 and p[1] >= 0 and p[0] < width and p[1] < height
	#return all([dim > loc for dim,loc in zip(size,point)]) #jacob wrote this hideous line of code and said fight me and its bad
	#return all([size[i] > point[i] for i in range(2)]) or min(point) =< 0

def distance(a, b):
	'''
	@params:
		a is a point-tuple
		b is another point-tuple
	returns a double representing distance between the two points
	'''
	return math.hypot(a[0] - b[0], a[1] - b[1])

def angleOf(vector):
	'''
	@params:
		vector is a vector-tuple
	returns a double representing the vectors clockwise rotation from the x axis
		values range from [0,2pi)
	'''
	at = math.atan2(vector[1], vector[0])
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
	if a < 0:
		a += 2 * math.pi
	return a

def kindaEquals(num1, num2, leniency=.2):
	'''
	@params
		num1 is a number
		num2 is also a number
		leniency is how lenient you're willing to be
	returns a boolean
		true if num1 is pretty close to num2
		false is num1 is pretty far from num2
	'''
	n2_max = num1*(1+leniency)
	n2_min = num1*(1-leniency)
	return num1 == num2 or n2 < n2_max and n2 > n2_min
