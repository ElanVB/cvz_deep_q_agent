from coord import Coord
from moveable import Moveable
from entity import Entity
import config
from random import randrange

class Environment():
	def __init__(self, num_humans, num_zombies):
		shooter = Entity(
			randrange(config.WIDTH), randrange(config.HEIGHT),
			config.SHOOTER_INTERACT_RANGE,
			config.SHOOTER_MOVE_RANGE
		)

		humans = dict()
		for i in range(num_humans):
			humans[i] = Coord(randrange(config.WIDTH), randrange(config.HEIGHT))

		zombies = dict()
		for i in range(num_zombies):
			zombies[i] = Entity(
				randrange(config.WIDTH), randrange(config.HEIGHT),
				config.ZOMBIE_INTERACT_RANGE,
				config.ZOMBIE_MOVE_RANGE
			)

		self.shooter = shooter
		self.humans = humans
		self.zombies = zombies
		self.score = 0
