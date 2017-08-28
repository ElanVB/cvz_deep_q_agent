import sys, time, hyperparams, random
import numpy as np
from environment import Environment
from renderer import Renderer
from keras_deep_q_agent import Agent

class Interface:
	def __init__(
		self, render=False, render_delay=0.03,
		max_humans=1, max_zombies=1, randomness=False,
		fine_tune=False, actions="default"
	):
		self._render = render
		if render:
			self._renderer = Renderer()
			self._render_delay = render_delay

		self._max_humans = max_humans
		self._max_zombies = max_zombies

		self._input_dim = 2 + 2*max_humans + 2*max_zombies

		if actions == "default":
			self._points = [(0, 0), (16000, 0), (0, 9000), (16000, 9000)]
			self._output_dim = len(self._points+1) # plus one for no-op
		else:
			raise ValueError("action value not supported")

		self._randomness = randomness
		self._fine_tune = fine_tune

	def initialize_agent(self, weights=None):
		self._agent = Agent(self._input_dim, self._output_dim)

		if weights != None:
			if not isinstance(weights, str):
				raise TypeError(
					"weights must be a string path to your weights file"
				)

			self._agent.load_weights(weights)

	def initialize_environment(self):
		humans = ranom.randrange(1, self._max_humans+1)\
			if self._randomness\
			else self._max_humans

		zombies = ranom.randrange(1, self._max_zombies+1)\
			if self._randomness\
			else self._max_zombies

		self.env = Environment(humans, zombies, better_rewards=True)
