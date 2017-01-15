#!/usr/bin/env python3
import mathutil



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

	def __hash__(self):
		return hash((self.x, self.y))

	def asTuple(self):
		return (self.x, self.y)

	def __add__(self, other): #Add with another point
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)

	def __rmul__(self, other): #Multiply by scalar number
		return Point(self.x * other, self.y * other)

	def distance(self, other):
		return math.hypot(self.x - other.x, self.y - other.y)

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
