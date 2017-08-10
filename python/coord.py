class Coord():
	def __init__(self, x, y):
		if not isinstance(x, (int, float)):
			raise TypeError("x must be an integer or a float")

		if not isinstance(y, (int, float)):
			raise TypeError("y must be an integer or a float")

		self.x = x
		self.y = y

	def __repr__(self):
		return "({}, {})".format(self.x, self.y)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		return NotImplemented

	def __ne__(self, other):
		if isinstance(other, self.__class__):
			return not self.__eq__(other)
		return NotImplemented

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))

	def copy(self):
		return Coord(x=self.x, y=self.y)

	def distance(self, coord):
		x_diff = self.x - coord.x
		y_diff = self.y - coord.y
		dist = (x_diff**2 + y_diff**2)**(0.5)

		return dist

	def key(self):
		return (self.x, self.y)
