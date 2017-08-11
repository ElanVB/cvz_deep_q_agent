# add speed? in interact_range
from moveable import Moveable

class Entity(Moveable):
	def __init__(self, x, y, interact_range, max_dist=None):
		if not isinstance(interact_range, (int, float)):
			raise TypeError("interact_range must be an integer or a float")

		self.interact_range = interact_range
		super().__init__(x=x, y=y, max_dist=max_dist)

	def copy(self):
		return Entity(x=self.x, y=self.y,
			interact_range=self.interact_range, max_dist=self.range)

	def __repr__(self):
		return super().__repr__() +\
			", interact_range: {}".format(self.interact_range)