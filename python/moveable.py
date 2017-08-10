from coord import Coord

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
