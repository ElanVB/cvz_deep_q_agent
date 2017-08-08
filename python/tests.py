import unittest
from coord import Coord
from moveable import Moveable

class CoordTestCase(unittest.TestCase):
	def setUp(self):
		self.test_x = 1
		self.test_y = 2
		self.coord = Coord(x=self.test_x, y=self.test_y)

	def tearDown(self):
		del self.coord

	def test_constructor(self):
		with self.assertRaises(TypeError):
			Coord(x="string", y="zz")

		with self.assertRaises(TypeError):
			Coord(x=(1.0, 1), y=0)

	def test_x_coord(self):
		self.assertEqual(self.test_x, self.coord.x)
		self.assertNotEqual(self.coord.x-1, self.coord.x)

	def test_y_coord(self):
		self.assertEqual(self.test_y, self.coord.y)
		self.assertNotEqual(self.coord.y-1, self.coord.y)

	def test_string_representation(self):
		self.assertEqual(
			"({}, {})".format(self.test_x, self.test_y), str(self.coord)
		)

	def test_copy(self):
		copy = self.coord.copy()
		self.assertEqual(self.coord.x, copy.x)
		self.assertEqual(self.coord.y, copy.y)
		self.assertEqual(str(self.coord), str(copy))

	def test_distance(self):
		copy = self.coord.copy()
		self.assertEqual(0, self.coord.distance(copy))
		self.assertEqual(0, self.coord.distance(self.coord))
		self.assertEqual(0, copy.distance(self.coord))
		self.assertEqual(0, copy.distance(copy))

		dist = 2**0.5
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=1, y=1)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=1, y=-1)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=-1, y=1)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=-1, y=-1)))

		dist = 2
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=0, y=2)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=0, y=-2)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=2, y=0)))
		self.assertEqual(dist, Coord(x=0, y=0).distance(Coord(x=-2, y=0)))

class MoveableTestCase(unittest.TestCase):
	def setUp(self):
		self.test_x = 1
		self.test_y = 2
		self.test_range = 3.0
		self.mover_a = Moveable(self.test_x, self.test_y)
		self.mover_b = Moveable(self.test_x, self.test_y, self.test_range)

	def tearDown(self):
		del self.mover_a
		del self.mover_b

	def test_constructor(self):
		with self.assertRaises(TypeError):
			Moveable((1, 2))

		with self.assertRaises(TypeError):
			Moveable(1, "asdf", max_dist=1.0)

		with self.assertRaises(TypeError):
			Moveable(1, 2, max_dist="asdf")

	def test_range(self):
		self.assertEqual(self.test_range, self.mover_b.range)
		self.assertNotEqual(self.test_range-1, self.mover_b.range)

	def test_coord(self):
		self.assertEqual(self.test_x, self.mover_a.x)
		self.assertEqual(self.test_y, self.mover_a.y)

if __name__ == "__main__":
    unittest.main()
