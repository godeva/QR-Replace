import math
from sklearn.cluster import AffinityPropagation

def clockwiseRotation(from_v, to_v):
	'''
	@params:
		from_v is a point representing a vector
		to_v is a point representing a vector
	returns a double representing the total rotation from vector from_v
		to the vector to_v. Value returned is in range [0,2pi).
		Used to determine which point is the "upper" clockwise leg of a triangle
	'''
	a = from_v.angleOf() - to_v.angleOf()
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
	return num1 == num2 or num2 < n2_max and num2 > n2_min
	#know your order of operations in boolean algebra
	#and is like multiplication or is like addition
	#we do it like this so if they are equal it jsut returns true and doesnt evaluate the rest
	#and then it evaluates the ands as if it had the perens



def slope(p1, p2):
	'''
	@params:
		p1 and p2 are point tuples
	returns the slope of a line drawn through p1 and p2
	'''
	return (p1.y-p2.y)/(p1.x-p2.x)


		#Cycle points
		last_point = next_point
		next_point = last_point + direction

	#Add last value to clusters
	ret_vals += [Segment(cluster_start, last_point)]
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

def extrapolateParallelogram(a, b, c):
	'''
	@params:
		a is one of the detected clusters in the image (as a point)
		b ditto
		c ditto
	returns a list of four points representing vertices of parallelogram
		in clockwise order. The new point is generated based on the previous 3.
	'''

	def deduceKnownCorner(a, b, c): #Get points as (corner, another, another)
		segs = (Segment(a,b), Segment(b,c), Segment(a,c))
		#Determine longest segment by sorting by lengths
		sorted_distance = sorted(segs, key=lambda seg: seg.length())
		longest_seg = sorted_distance[2]

		#Find the points in longest seg, sort by being in it
		#Ascending sort will put remaining at back
		ls_points = (longest_seg.p1, longest_seg.p2)
		return sorted((a,b,c), key=lambda p: p in ls_points)

	def orderByRotation(a, b, c): #Orders points of triangle clockwise. First point is anchor. Tuple of tuple-point
		cp = deduceKnownCorner(a,b,c)
		corner = cp[0]
		a = cp[1]
		b = cp[2]

		#Get vectors from corner to each leg
		v_corner_a = a - corner
		v_corner_b = b - corner

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
		vec_corner_leg1 = leg1 - corner

		#Add this vec to leg2 to get final point of pgram.
		return leg2 + vec_corner_leg1

	op = orderByRotation(a,b,c)
	np = genThirdPoint(op)
	parallelogram = (op[0], op[1], np, op[2])

	#Reorder to have first point be top-leftmost
	origin = Point(0,0)
	offsets = [origin.distance(x) for x in parallelogram]
	closest_index = offsets.index(min(offsets))
	return parallelogram[closest_index:] + parallelogram[:closest_index]

def expandParallelogram(parallelogram, amount):
	'''
	@params:
		parallelogram is the parllelogram to expand
		amount is the amount it should be expanded by
	returns a new parallelogram that is slightly larger
		**Note that parallelograms must be named starting from upper left
		and proceed clockwise
	'''
	UL = addTuples(parallelogram[0], (-amount,-amount))
	UR = addTuples(parallelogram[1], (amount,-amount))
	LR = addTuples(parallelogram[2], (amount,amount))
	LL = addTuples(parallelogram[3], (-amount,amount))

	return (UL, UR, LR, LL)

def constructParallelograms(dataset):
	'''
	@params
		dataset is a list of points to find clusters in
	returns a list of the parallelograms found.
	'''
	af = AffinityPropagation().fit(dataset)
	print(af.cluster_centers_, af.labels_, len(af.cluster_centers_))
	clusters = []
	count = 0
	while (count < len(af.cluster_centers_)):
		clusters += [af.cluster_centers_[count].tolist()]
		count += 1

	print(clusters)
	return extrapolateParallelogram(clusters[0], clusters[1], clusters[2])
