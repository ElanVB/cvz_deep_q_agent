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

	def move_zombies(self):
		for zombie_id in self.zombies:
			min_dist = self.zombies[zombie_id].distance(self.shooter)
			min_pos = self.shooter
			for human_id in self.humans:
				dist = self.zombies[zombie_id].distance(self.humans[human_id])
				if dist < min_dist:
					min_dist = dist
					min_pos = self.humans[human_id]

			self.zombies[zombie_id].move(min_pos.x, min_pos.y)
			self.zombies[zombie_id].x = int(self.zombies[zombie_id].x)
			self.zombies[zombie_id].y = int(self.zombies[zombie_id].y)

	def move_shooter(self, x, y):
		self.shooter.move(x, y)
		self.shooter.x = int(self.shooter.x)
		self.shooter.y = int(self.shooter.y)

	def shoot_zombies(self):
		zombies_killed = 0
		dead_ids = []
		for zombie_id in self.zombies:
			if self.shooter.in_range(self.zombies[zombie_id]):
				zombies_killed += 1
				dead_ids.append(zombie_id)

		for zombie_id in dead_ids:
			del self.zombies[zombie_id]

		if zombies_killed > 0:
			self.score += self.round_score(len(self.humans), zombies_killed)
