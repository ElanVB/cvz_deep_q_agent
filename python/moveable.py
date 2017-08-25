from coord import Coord
import math

class Moveable(Coord):
	def __init__(self, x, y, max_dist=None):
		if max_dist != None and not isinstance(max_dist, (int, float)):
			raise TypeError("max_dist must be an integer or a float")

		self.range = max_dist
		super().__init__(x=x, y=y)

	def copy(self):
		return Moveable(x=self.x, y=self.y, max_dist=self.range)

	def __repr__(self):
		string = super().__repr__()
		string += " - range: {}".format(self.range) if self.range != None else ""
		return string

	def move(self, x, y):
		if not isinstance(x, (int, float)):
			raise TypeError("x must be an integer or a float")

		if not isinstance(y, (int, float)):
			raise TypeError("y must be an integer or a float")

		if self.range != None:
			dist = self.distance(Coord(x=x, y=y)) # this may be in inefficient
			if dist <= self.range: # this if hasn't been tested...
				self.x = x
				self.y = y
			else:
				angle = math.atan2(y - self.y, x - self.x)
				x_inc = self.range * math.cos(angle)
				y_inc = self.range * math.sin(angle)
				self.x += x_inc
				self.y += y_inc
		else:
			self.x = x
			self.y = y
