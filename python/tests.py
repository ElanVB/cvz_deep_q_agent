import unittest
from coord import Coord

class CoordTestCase(unittest.TestCase):
	def setUp(self):
		self.coord = Coord(x=1, y=2)

	def tearDown(self):
		del self.coord

	def test_x_coord(self):
		self.assertEqual(1, self.coord.x)

	def test_y_coord(self):
		self.assertEqual(2, self.coord.y)

if __name__ == '__main__':
    unittest.main()
