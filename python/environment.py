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
		self.fibonacci_seq = [1, 1, 2]

	def fibonacci(self, n):
		if n <= len(self.fibonacci_seq):
			return self.fibonacci_seq[n-1]

		for _ in range(n - len(self.fibonacci_seq)):
			self.fibonacci_seq.append(
				self.fibonacci_seq[-1] + self.fibonacci_seq[-2]
			)

		return self.fibonacci_seq[-1]

	def round_score(self, alive_humans, zombies_killed):
		human_score = 10 * (alive_humans**2)
		zombie_score = 0
		for i in range(zombies_killed):
			zombie_score += self.fibonacci(i+2)

		return human_score * zombie_score
