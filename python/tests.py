import unittest
from coord import Coord

class CoordTestCase(unittest.TestCase):
	def setUp(self):
		self.test_x = 1
		self.test_y = 2
		self.coord = Coord(x=self.test_x, y=self.test_y)

	def tearDown(self):
		del self.coord

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

if __name__ == "__main__":
    unittest.main()
