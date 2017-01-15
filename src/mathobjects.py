#!/usr/bin/env python3
import mathutil
import math

class Point:
	'''
	its a point
	'''
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def equals(self, point):
		'''
		@params:
			point is another point
		returns true if the points have same x and y values
		false otherwise
		'''
		return self.x == point.x and self.y == point.y

	def __str__(self):
		return "({},{})".format(self.x, self.x)

	def __hash__(self):
		return hash((self.x, self.y))

	def asTuple(self):
		return (self.x, self.y)

	def __add__(self, other): #Add with another point
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)#Subtract another point

	def __rmul__(self, other): #Multiply by scalar number
		return Point(self.x * other, self.y * other)

	def distance(self, other):
		return math.hypot(self.x - other.x, self.y - other.y)

	def angleOf(self):
		'''
		returns a double representing this point's (as a vector),
			['s] counter-clockwise rotation from the x axis
			values range from [0,2pi)
		'''
		at = math.atan2(self.y, self.x)
		if at < 0:
			at += 2*math.pi
		return at

	def isInBounds(self, image):
		'''
		@params:
			image is the image that we'll be checking with
		returns a boolean
			True if this point is inside the image
			False if this point is outside the image
		'''
		width, height = image.size
		p = self
		return p.x >= 0 and p.y >= 0 and p.x < width and p.y < height


class Line:
	'''
	its a line, defined by its slope and y intercept
	'''
	def __init__(self, p1, p2):
		self.slope = mathutil.slope(p1, p2)
		self.intercept = p1[1] - slope*p1[0] #the y intercept of the line

	def contains(self, point):
		'''
		@params:
			point is a point-tuple
		returns true if point is on the line
		otherwise gives false
		'''
		return point.y == slope*point.x + intercept

	def equals(self, line):
		'''
		is it that hard to guess what this does?
		'''
		return self.slope == line.slope and self.intercept == line.intercept

class Segment:
	'''
	Class representing a simple line segment composed of two points
	'''
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def __str__(self):
		return "<{}-{}>".format(self.p1, self.p2)

	def equals(self, segment):
		return p1.equals(segment.p1) and p2.equal(segment.p2)

	def length(self):
		return self.p1.distance(self.p2)

	def midpoint(self):
		return 0.5 * (self.p1 + self.p2)
