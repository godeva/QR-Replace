#!/usr/bin/env python3
from PIL import Image
import qrcode
import numpy as np
from numpy.linalg import inv
import itertools
from mathutil import *

'''
NOTE:
color-tuples are 3 element tuples structred as (R,G,B), 0-255 each

point-tuples are 2 element tuples structed as (x,y) @todo(someone) make a point class or
(note that this is consistent with pillows use of points)
vectors are equivalent to point-tuples, but with a different context
cluster-tuple is a (point-tuple, int) where the int is cluster size

quadrilateral-tuples are 4 element tuples structured as (point-tuple,point-tuple,point-tuple,point-tuple)
'''


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
		p1 is a point
		p2 is a point

	Delegate call to diffColors on two points in an image
	'''
	a = image.getpixel(p1.asTuple())
	b = image.getpixel(p2.asTuple())
	return diffColors(a,b)

def getColorGroups(image, start, direction):
	'''
	@params:
		image is the PIL image to sample from
		start is a point defining where to begin scanning clusters
		direction is a point (vector) defining direction to travel

	Scan over an image from a starting point until end of image is reached.
	Scan results are returned as a list of Segments
	EX:
	[Segment, Segment]

	direction as a vector allows this function to be used for vertical, horizontal,
	diagonal, or any angle of traversal, at varying levels of precision.
	'''
	ret_vals = [] #Create list to add clusters to
	last_point = start
	next_point = last_point + direction

	#Track current cluster
	cluster_start = last_point

	threshold = 50
	#Continue scanning until curr_point is outside of image
	while next_point.isInBounds(image):
		delta = diffPoints(image, last_point, next_point)

		#Check if delta above thresh. If so, break off segment
		if delta > threshold:
			#Else, add to ret vals
			ret_vals += [Segment(cluster_start, last_point)]
			cluster_start = next_point

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

def warpImage(background, image, parallelogram):
	'''
	@params:
		background is unchanged image
		image is image to be warped
		parallelogram is the coordinates to warp the image to, starting at upper
			left and going clockwise
	returns a new image that is the composition of background and image
	 	after image has been warped
	'''
	mapped = np.array([[parallelogram[0][0], parallelogram[1][0], parallelogram[2][0]],
	[parallelogram[0][1], parallelogram[1][1], parallelogram[2][1]], [1,1,1]])
	width, height = image.size
	original = np.array([[0, width, width],[0, 0, height]])
	#solve for affine matrix
	solution = np.dot(original, inv(mapped))
	#unroll matrix into a sequence
	affine = (solution[0][0], solution[0][1], solution[0][2], solution[1][0], solution[1][1], solution[1][2])
	transformed = image.transform(background.size, Image.AFFINE, affine)
	white = Image.new("RGBA", (width, height), "white")
	transformedMask = white.transform(background.size, Image.AFFINE, affine)
	background.paste(transformed, (0,0), transformedMask)
	return background

def getImageQRClusters(image, scan_vector):
	'''
	@params:
		image is the image to search for qr-clusters on
		scan_vector is a vector direction to traverse the image along.
	returns a list of points representing the center of group-tuple strips satisfying
		the QR code ratio.
	'''
	candidates = []
	width = image.size[0]
	height = image.size[1]

	#Determine what generator to use to generate scanline starts
	starts = []

	#Create generators for each edge. Will use either depending on
	top_edge   = (Point(x,0) for x in range(width))
	left_edge  = (Point(0,y) for y in range(height))
	bot_edge   = (Point(x, height-1) for x in range(width))
	right_edge = (Point(width-1,  y) for y in range(height))

	#If scan vector leftwards, need right edge. Etc.
	if scan_vector[0] < 0:
		starts = itertools.chain(starts, left_edge)
	elif scan_vector[0] > 0:
		starts = itertools.chain(starts, right_edge)
	#Do same for verticals
	if scan_vector[1] < 0:
		starts = itertools.chain(starts, top_edge)
	elif scan_vector[1] > 0:
		starts = itertools.chain(starts, bot_edge)

	#For each start point select candidates
	for start in starts:
		#Gen groups from this start
		groups = getColorGroups(image, start, scan_vector)

		#Zip through sets of 5 groups to find 1:1:3:1:1
		group_sets = (groups[i:] for i in range(5))
		for scan_set in zip(*group_sets):
			#Compute lengths of each seg
			scan_lengths = [distance(*scan_part) for scan_part in scan_set]

			#Get length of first segnment as a  baseline to compare rest
			base_len = scan_lengths[0]

			#Since ratio is 1:1:3:1:1, adjust 3rd elt to be 1 so easier to compare
			scan_lengths[2] /= 3

			#Now check if all roughly equal
			if all(kindaEquals(base_len, length) for length in scan_lengths):
				center_set = scan_set[2]
				#compute midpoint of center_set

				center_mid = (x_avg, y_avg)
				candidates.append(center_mid)

	return candidates

def getMassQRClusters(image, num_vectors):
	'''
	@params:
		image is the image to scan,
		num_vectors is the number of different vectors to scan along
	returns the combined result of running getImageQRClusters over the image from
		many different angles, to counteract possible rotational artifacts.
	'''
	angle_delta = math.pi / num_vectors
	vec_angles = [x*angle_delta for x in range(num_vectors)]
	vectors = [(cos(theta), sin(theta)) for theta in vec_angles]

	#Generate points for each vector
	qr_points = []
	for vec in vectors:
		qr_points += getImageQRClusters(image, vec)

	return qr_points

def scanImage(image):
	'''
	@params
		image is the image that we'll be messing with
	returns a list of tuple-points which are the centers of any QR code corner identifiers
	'''
	#lineclusters will be a list of lists (one per horizontal line) of cluster-tuples
	print(image.size[1])
	lineclusters = [getPixelClusters(image, (0,i), (1,0)) for i in range(image.size[1])]
	lineclusters = []
	for i in range(image.size[1]):
		lineclusters.append(getPixelClusters(image, (0,i), (1,0)))
	iclusters = [] #interesting clusters
	for line in lineclusters:
		matches = []
		print("line{}".format(line))
		if len(line) < 5:
			iclusters.append(matches)
			continue

		for i in range(len(lineclusters)-4): #scan the clusters five at a time to find the QR pattern
			scanthis = line[i:i+5]	 #we're looking for 1-1-3-1-1
			#print(scanthis)
			if len(scanthis) < 5:
			 	continue
			baselen = len(scanthis[0])
			if kindaEquals(baselen, scanthis[1][1]) and kindaEquals(baselen, scanthis[3][1]) and kindaEquals(baselen, scanthis[4][1]) and kindaEquals(baselen*3, scanthis[2][1]): #i'm so sorry for this line of code. basically it just checks for the 1 1 3 1 1 pattern in qr code corners
				matches.append(scanthis[3][1][0]/2 + scanthis[3][1][0]) #adds the middle of the middle of the scan to the matches
		iclusters.append(matches)
	cluster_points = [] #this is a list of cluster points that we will be returning
	current_line = -1 #we start at -1 because i do +1 at the beginning
	while current_line < image.size[1]-1:
		current_line = current_line + 1
		if len(iclusters[current_line]) < 0:
			continue #so that i can just do this lazy line of code
		scanline = current_line
		for current_col in iclusters[current_line]: #this for loop handles when there's two clusters in one row (bottom of QR code)
			scanline = current_line #we sometimes need to scanline down twice
			while len(iclusters[scanline] > 0) and kindaEquals(iclusters[scanline], current_line): #make sure that the clusters match up
				scanline = scanline + 1
			cluster_center = (current_col, int((scanline - current_line)/2)) #current_col is the position in the row
			cluster_points.append(cluster_center)							#scanline is end of the cluster, current_line is beginning so we can take their mean to get the middle
		current_line = scanline #after scanning the clusters we set current line to scanline
									#if we get lots of very nearby points change previous line to blabla = scanline + 1
	return cluster_points

	def simplifyPoints(points):
		'''
		@param
			points is an iterable containing many point-tuples
		ok so like. find clusters of points. points are always gonna be basically in the same line
		this is gonna be a bad code
		im sorry future me who has to maybe delete this
		i'll do lots of comments (i hope)
		'''
		#pass #@todo(aaronn) implement this. goal is to have it working by 1am
		'''
		LMAO OK
		so the plan is to make "clusters" of colinear ones
		then we break up the clusters if there's blank space
		then we kill any cluster that's really small
		then we can just take the mean of the points
		'''
		'''
		ok so the structure of one of these clusters im just gonn make a class
		'''
		clusters = []
		prevpoint = points[0]
		for i in range(1,len(points)):
			newcluster = LineCluster(prevpoint,points[i])
			if not all(newcluster.equals(cluster) for cluster in clusters) or len(clusters) == 0:
				clusters.append(newline)
				for point in points[i:-1]:
					newcluster.add

class LineCluster:
	def __init__(self,p1,p2):
		self.members = [p1,p2]
		self.line = Line(p1,p2)

	def add(point):
		'''
		@params:
			point is a tuple point
		adds the point to the linecluster if
		'''
		if line.contains(point):
			members.append(point)
		return

	def size(self):
		return len(self.members)

	def shortestDistance(self):
		'''
		returns the shortest distance between any two points in the line
		'''
		return min([distance(p1,p2) for p1 in members for p2 in members if p1])

	def equals(cluster):
		return self.line.equals(cluster.line)
