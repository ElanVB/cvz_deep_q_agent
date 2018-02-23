from interface import Interface
from environment import Environment
from renderer import Renderer
import random, time

class Match():
	def __init__(self, max_humans=2, max_zombies=3, randomness=True, render_delay=0.05):
		self._max_humans = max_humans
		self._max_zombies = max_zombies
		self._randomness = randomness
		self._env = Environment()

		self._render_delay = render_delay
		self._renderer = Renderer(two_player=True)

	def draw_environment(self, env1, env2):
		self._renderer.draw_environment(env1)
		self._renderer.draw_environment(env2, player_two=True)

	def wait(self, delay_time=None):
		if delay_time == None:
			time.sleep(self._render_delay)
		else:
			time.sleep(delay_time)

	def initialize_environment(
			self, num_humans=None, num_zombies=None, randomness=True
		):
			if num_humans == None:
				num_humans = self._max_humans

			if num_zombies == None:
				num_zombies = self._max_zombies

			if randomness and self._randomness:
				humans = random.randrange(1, num_humans+1)
				zombies = random.randrange(1, num_zombies+1)
			else:
				humans = num_humans
				zombies = num_zombies

			self._env.reset(humans, zombies)

	def get_mouse_pos(self):
		return self._renderer.get_mouse_pos()

	def update_environment(self, env, coord_tuple):
		x, y = coord_tuple
		x, y = (x / self._renderer._x_scale, y / self._renderer._y_scale)
		env.update(x, y)

	def play_game(self, agent):
		self.initialize_environment()

		human_env = self._env.copy()
		agent_env = self._env.copy()
		agent._env = agent_env

		agent_state = agent.get_state_sequence()

		self.draw_environment(human_env, agent_env)
		self.wait(0.5)

		while(not (human_env.is_done() and agent_env.is_done())):
			self.draw_environment(human_env, agent_env)

			start_time = time.time()

			current_time = time.time()
			while(current_time - start_time < self._render_delay):
				current_time = time.time()
				mouse_pos = self.get_mouse_pos()

			self.update_environment(human_env, mouse_pos)
			agent_state, _ = agent.agent_on_policy_act(agent_state)

		self.draw_environment(human_env, agent_env)
		self.wait(1)
		self._renderer.draw_winner(human_env.score, agent._env.score)
		print("Human: {}, Agent: {}".format(human_env.score, agent._env.score))
		self._renderer.freeze()

	def play_rounds(self, num_rounds=5):
		agent = Interface(max_humans=2, max_zombies=3)
		agent.initialize_agent(weights="2_3_demo")

		# for i in range(num_rounds):
		while(True):
			self.play_game(agent)

# Test
p = Match()
p.play_rounds()