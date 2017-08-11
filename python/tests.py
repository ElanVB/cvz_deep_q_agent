import unittest
from coord import Coord
from moveable import Moveable
from entity import Entity
import math

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
		self.assertEqual(copy, self.coord)

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
		self.test_x = 0
		self.test_y = 0
		self.test_range = 3.0
		self.mover_a = Moveable(x=self.test_x, y=self.test_y)
		self.mover_b = Moveable(x=self.test_x, y=self.test_y,
			max_dist=self.test_range)

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

	def test_position(self):
		self.assertEqual(self.test_x, self.mover_a.x)
		self.assertEqual(self.test_y, self.mover_a.y)

	def test_copy(self):
		copy_a = self.mover_a.copy()
		copy_b = self.mover_b.copy()

		self.assertEqual(copy_a, self.mover_a)
		self.assertNotEqual(copy_a, self.mover_b)

		self.assertEqual(copy_b, self.mover_b)
		self.assertNotEqual(copy_b, self.mover_a)

	def test_distance(self):
		copy = self.mover_a.copy()
		self.assertEqual(0, self.mover_a.distance(copy))
		self.assertEqual(0, self.mover_a.distance(self.mover_a))
		self.assertEqual(0, copy.distance(self.mover_a))
		self.assertEqual(0, copy.distance(copy))

		dist = 2**0.5
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=1, y=1)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=1, y=-1)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=-1, y=1)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=-1, y=-1)))

		dist = 2
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=0, y=2)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=0, y=-2)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=2, y=0)))
		self.assertEqual(dist, Moveable(x=0, y=0).distance(Moveable(x=-2, y=0)))

	def test_string_representation(self):
		self.assertEqual(
			"({}, {})".format(self.test_x, self.test_y), str(self.mover_a)
		)

		self.assertEqual(
			"({}, {}) - range: {}".format(self.test_x, self.test_y, self.test_range),
			str(self.mover_b)
		)

	def test_move(self):
		x = 100
		y = -100
		self.mover_a.move(x, y)
		self.assertEqual(
			Moveable(x, y), self.mover_a
		)

		self.mover_b.move(x, y)
		self.assertEqual(
			self.mover_b.distance(Coord(self.test_x, self.test_y)),
			self.test_range
		)

		self.assertEqual(
			self.mover_b, Moveable(
				self.test_x + self.test_range * math.cos(-math.pi/4),
				self.test_y + self.test_range * math.sin(-math.pi/4),
				self.test_range
			)
		)

		pos = self.mover_b.copy()
		self.mover_b.move(self.test_x, self.test_y)
		self.assertEqual(
			self.mover_b.distance(pos),
			self.test_range
		)

		self.assertEqual(
			self.mover_b, Moveable(
				round(pos.x + self.test_range * math.cos(math.pi-math.pi/4), 9),
				round(pos.y + self.test_range * math.sin(math.pi-math.pi/4), 9),
				self.test_range
			)
		)

		x = -4365.23453
		y = 12.23452
		self.mover_a.move(x, y)
		self.assertEqual(
			Moveable(x, y), self.mover_a
		)

		mover_b_before = self.mover_b.copy()
		self.mover_b.move(x, y)
		self.assertEqual(
			self.mover_b.distance(Coord(self.test_x, self.test_y)),
			self.test_range
		)

		pos = self.mover_b.copy()
		self.mover_b.move(self.test_x, self.test_y)
		self.assertEqual(
			self.mover_b.distance(pos),
			self.test_range
		)

		self.assertEqual(self.mover_b, mover_b_before)

class EntityTestCase(unittest.TestCase):
	def setUp(self):
		self.test_x = 0
		self.test_y = 0
		self.test_move_range = 100.0
		self.test_interact_range = 200.0
		self.entity = Entity(
			x=self.test_x, y=self.test_y,
			interact_range=self.test_interact_range,
			max_dist=self.test_move_range
		)

	def tearDown(self):
		del self.entity

	def test_constructor(self):
		with self.assertRaises(TypeError):
			Entity((1, 2))

		with self.assertRaises(TypeError):
			Entity(1, "asdf", max_dist=1.0)

		with self.assertRaises(TypeError):
			Entity(1, 2, max_dist="asdf")

		with self.assertRaises(TypeError):
			Entity(1, 2, max_dist=10)

		with self.assertRaises(TypeError):
			Entity(1, 2, "93", max_dist=10)

	def test_position(self):
		self.assertEqual(self.test_x, self.entity.x)
		self.assertEqual(self.test_y, self.entity.y)

	def test_copy(self):
		copy_a = self.entity.copy()
		self.assertEqual(copy_a, self.entity)

	def test_string_representation(self):
		self.assertEqual(
			"({}, {}) - range: {}, interact_range: {}"
				.format(
					self.test_x, self.test_y, self.test_move_range,
					self.test_interact_range
				),
			str(self.entity)
		)

	def test_move(self):
		x = 100
		y = -100
		self.entity.move(x, y)
		self.assertEqual(
			round(self.entity.distance(Coord(self.test_x, self.test_y)), 9),
			self.test_move_range
		)

		self.assertEqual(
			self.entity, Entity(
				self.test_x + self.test_move_range * math.cos(-math.pi/4),
				self.test_y + self.test_move_range * math.sin(-math.pi/4),
				self.test_interact_range,
				self.test_move_range
			)
		)

		pos = self.entity.copy()
		self.entity.move(self.test_x, self.test_y)
		self.assertEqual(
			round(self.entity.distance(pos), 9),
			self.test_move_range
		)

		self.assertEqual(
			self.entity, Entity(
				round(pos.x + self.test_move_range * math.cos(math.pi-math.pi/4), 9),
				round(pos.y + self.test_move_range * math.sin(math.pi-math.pi/4), 9),
				self.test_interact_range,
				self.test_move_range
			)
		)

		x = -4365.23453
		y = 12.23452
		entity_before = self.entity.copy()
		self.entity.move(x, y)
		self.assertEqual(
			self.entity.distance(Coord(self.test_x, self.test_y)),
			self.test_move_range
		)

		pos = self.entity.copy()
		self.entity.move(self.test_x, self.test_y)
		self.assertEqual(
			self.entity.distance(pos),
			self.test_move_range
		)

		self.assertEqual(self.entity, entity_before)

if __name__ == "__main__":
    unittest.main()
