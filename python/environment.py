from coord import Coord
from moveable import Moveable
from entity import Entity
from random import randrange
import config, math, numpy as np

class Environment():
	def __init__(self, num_humans=0, num_zombies=0, better_rewards=True, simple_rewards=False):
		if not isinstance(num_humans, int):
			raise TypeError("num_humans must be an integer")

		if not isinstance(num_zombies, int):
			raise TypeError("num_zombies must be an integer")

		if not isinstance(better_rewards, bool):
			raise TypeError("better_rewards must be a boolean")

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
		self.reward = 0
		self._better_rewards = better_rewards
		self._simple_rewards = simple_rewards
		self._fibonacci_seq = [1, 1, 2]

		if better_rewards:
			self._max_reward = self._round_score(num_humans, num_zombies)

		self._done = False
		self._round = 0

	def _fibonacci(self, n):
		if n <= len(self._fibonacci_seq):
			return self._fibonacci_seq[n-1]

		for _ in range(n - len(self._fibonacci_seq)):
			self._fibonacci_seq.append(
				self._fibonacci_seq[-1] + self._fibonacci_seq[-2]
			)

		return self._fibonacci_seq[-1]

	def _round_score(self, alive_humans, zombies_killed):
		human_score = 10 * (alive_humans**2)
		zombie_score = 0
		for i in range(zombies_killed):
			zombie_score += self._fibonacci(i+2)

		return human_score * zombie_score

	def _move_zombies(self):
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

	def _move_shooter(self, x, y):
		x = min(x, config.WIDTH-1)
		y = min(y, config.HEIGHT-1)
		
		self.shooter.move(x, y)
		self.shooter.x = int(self.shooter.x)
		self.shooter.y = int(self.shooter.y)

	def _shoot_zombies(self):
		zombies_killed = 0
		dead_ids = []
		for zombie_id in self.zombies:
			if self.shooter.in_range(self.zombies[zombie_id]):
				zombies_killed += 1
				dead_ids.append(zombie_id)

		for zombie_id in dead_ids:
			del self.zombies[zombie_id]

		if zombies_killed > 0:
			self.reward = self._round_score(len(self.humans), zombies_killed)
			self.score += self.reward

		if self._better_rewards:
			self.reward /= self._max_reward

		if len(self.zombies) == 0:
			self.reward = 1

		if self._simple_rewards:
			if zombies_killed > 0:
				self.reward = 1
			else:
				self.reward = 0

	def _eat_humans(self):
		# if self._better_rewards:
		dead_count = 0

		for zombie_id in self.zombies:
			dead_ids = []
			for human_id in self.humans:
				if self.zombies[zombie_id].in_range(self.humans[human_id]):
					dead_ids.append(human_id)

			for human_id in dead_ids:
				self.zombies[zombie_id].x = self.humans[human_id].x
				self.zombies[zombie_id].y = self.humans[human_id].y
				del self.humans[human_id]

			if self._better_rewards:
				dead_count += len(dead_ids)

		# if self._better_rewards and dead_count > 0:
		# 	live_humans = len(self.humans)
		# 	num_zombies = len(self.zombies)
		# 	self.reward -= (
		# 		self._round_score(live_humans+dead_count, num_zombies) -
		# 		self._round_score(live_humans, num_zombies)
		# 	)

		if len(self.humans) == 0:
			# self.reward -= self.score
			self.score = 0

		if self._better_rewards and dead_count > 0:
			# self.reward = -1
			live_humans = len(self.humans)
			num_zombies = len(self.zombies)
			self.reward = -(
				self._round_score(live_humans+dead_count, num_zombies) -
				self._round_score(live_humans, num_zombies)
			) / self._max_reward

		if len(self.humans) == 0:
			self.reward = -1

		if self._simple_rewards:
			if dead_count > 0:
				self.reward = -1
			else:
				self.reward = 0

	def is_done(self):
		return self._done or len(self.humans) == 0 or len(self.zombies) == 0

	def update(self, x, y):
		if not isinstance(x, (int, float)):
			raise TypeError("x must be an integer or a float")

		if not isinstance(y, (int, float)):
			raise TypeError("y must be an integer or a float")

		self.reward = 0
		self._move_zombies()
		self._move_shooter(x, y)
		self._shoot_zombies()
		self._eat_humans()

		# if self._better_rewards:
		# 	self.reward /= self._max_reward

		if not self._simple_rewards and self.reward == 0:
			live_humans = len(self.humans)
			num_zombies = len(self.zombies)
			self.reward = -0.1 * (
				self._round_score(live_humans, num_zombies) -
				self._round_score(live_humans-1, num_zombies)
			) / self._max_reward

		self._round += 1
		if self._round >= 200:
			self._done = True

	def parse_state_file(self, filename):
		state_file = open(filename, "r")
		file_lines = state_file.readlines()
		state_file.close()

		state = dict()
		x, y = [int(i) for i in file_lines[0].split(" ")]
		state["shooter"] = Entity(
			x, y,
			config.SHOOTER_INTERACT_RANGE,
			config.SHOOTER_MOVE_RANGE
		)

		num_humans = int(file_lines[1])
		counter = 2
		state["humans"] = dict()
		for i in range(num_humans):
			id_num, x, y = [int(i) for i in file_lines[i+counter].split(" ")]
			state["humans"][id_num] = Coord(x, y)

		counter += num_humans
		num_zombies = int(file_lines[counter])
		counter += 1
		state["zombies"] = dict()
		for i in range(num_zombies):
			id_num, x, y = [int(i) for i in file_lines[i+counter].split(" ")]
			state["zombies"][id_num] = Entity(
				x, y,
				config.ZOMBIE_INTERACT_RANGE,
				config.ZOMBIE_MOVE_RANGE
			)

		return state

	def copy(self):
		new_env = Environment()
		new_env.shooter = self.shooter.copy()
		new_env.humans = {i: h.copy() for i, h in self.humans.items()}
		new_env.zombies = {i: z.copy() for i, z in self.zombies.items()}
		new_env._max_reward = self._max_reward

		new_env.score = self.score
		new_env.reward = self.reward
		new_env._better_rewards = self._better_rewards
		new_env._simple_rewards = self._simple_rewards
		new_env._fibonacci_seq = [i for i in self._fibonacci_seq]
		new_env._done = self._done
		new_env._round = self._round

		return new_env

	def load_state(self, state):
		self._load_state(
			state["shooter"].copy(),
			{h: state["humans"][h].copy() for h in state["humans"]},
			{z: state["zombies"][z].copy() for z in state["zombies"]}
		)

	def _load_state(self, shooter, humans, zombies):
		if not isinstance(shooter, Entity):
			raise TypeError("shooter must be of type Entity")

		if not isinstance(humans, dict):
			raise TypeError("humans must be a dictionary")

		if not isinstance(zombies, dict):
			raise TypeError("zombies must be a dictionary")

		for human_id in humans:
			if not isinstance(humans[human_id], Coord):
				raise TypeError(
					"humans must contain only objects of type Coord"
				)

		for zombie_id in zombies:
			if not isinstance(zombies[zombie_id], Entity):
				raise TypeError(
					"zombies must contain only objects of type Entity"
				)

		self.shooter = shooter
		self.humans = humans
		self.zombies = zombies
		self.score = 0
		self.reward = 0
		self._done = False
		self._round = 0

		if self._better_rewards:
			self._max_reward = self._round_score(len(humans), len(zombies))

	def get_state_variables(self, entity):
		return [
			entity.x / config.WIDTH,
			entity.y / config.HEIGHT
		]

	def get_state(self):
		state = []
		state += self.get_state_variables(self.shooter)

		for i in range(99):
			if i not in self.humans:
				state += [-1, -1]
			else:
				state += self.get_state_variables(self.humans[i])

		for i in range(99):
			if i not in self.zombies:
				state += [-1, -1]
			else:
				state += self.get_state_variables(self.zombies[i])

		return state

	def draw(self, grid, value, radius, h, w):
		scale_factor = config.STATE_IMAGE_SCALE
		grid_width = math.ceil(config.WIDTH * scale_factor)
		grid_height = math.ceil(config.HEIGHT * scale_factor)

		radius = int(radius)

		grid[h][w] = value
		for inc_h in range(-radius, radius+1):
			for inc_w in range(-radius, radius+1):
				if h+inc_h < grid_height and h+inc_h >= 0 and w+inc_w < grid_width and w+inc_w >= 0:
					if Coord(inc_h, inc_w).distance(Coord(0, 0)) <= radius:
						grid[h+inc_h][w+inc_w] = value

		return grid

	def get_state_image(self, type="grayscale"):
		scale_factor = config.STATE_IMAGE_SCALE
		grid_width = math.ceil(config.WIDTH * scale_factor)
		grid_height = math.ceil(config.HEIGHT * scale_factor)

		grid = np.zeros((grid_height, grid_width))

		values = config.STATE_IMAGE_VALUES
		# draw humans
		for _, human in self.humans.items():
			w = int(human.x * scale_factor)
			h = int(human.y * scale_factor)
			grid = self.draw(grid, values["human"], config.ZOMBIE_INTERACT_RANGE * scale_factor, h, w)

		# draw zombies
		for _, zombie in self.zombies.items():
			w = int(zombie.x * scale_factor)
			h = int(zombie.y * scale_factor)
			grid = self.draw(grid, values["zombie"], config.ZOMBIE_INTERACT_RANGE * scale_factor, h, w)

		# draw shooter
		w = int(self.shooter.x * scale_factor)
		h = int(self.shooter.y * scale_factor)
		grid = self.draw(grid, values["shooter"], config.SHOOTER_INTERACT_RANGE * scale_factor, h, w)

		return grid

	def reset(self, num_humans=None, num_zombies=None):
		###################################################
		if num_humans == None:
			num_humans = len(self.humans) # this does not work

		if num_zombies == None:
			num_zombies = len(self.zombies) # this does not work
		###################################################

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
		self.reward = 0

		if self._better_rewards:
			self._max_reward = self._round_score(num_humans, num_zombies)

		self._done = False
		self._round = 0
