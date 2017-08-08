class Coord():
	def __init__(self, x, y):
		if type(x) is not int:
			raise TypeError("x must be an integer")

		if type(y) is not int:
			raise TypeError("y must be an integer")

		self.x = x
		self.y = y

	def __repr__(self):
		return str(
			"({}, {})".format(self.x, self.y)
		)

	def copy(self):
		return Coord(x=self.x, y=self.y)

	def distance(self, coord):
		x_diff = self.x - coord.x
		y_diff = self.y - coord.y
		dist = (x_diff**2 + y_diff**2)**(0.5)

		return dist
