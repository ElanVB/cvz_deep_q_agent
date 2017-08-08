from coord import Coord

class Moveable(Coord):
	def __init__(self, x, y, max_dist=None):
		if max_dist != None:
			if not isinstance(max_dist, (int, float)):
				raise TypeError("max_dist must be an integer or a float")

			self.range = max_dist

		super().__init__(x=x, y=y)
