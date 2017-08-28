import sys, time, hyperparams, random, collections
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
			self._output_dim = len(self._points)
			# self._output_dim = len(self._points)+1 # plus one for no-op
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

		self._env = Environment(humans, zombies, better_rewards=True)

	def get_state(self):
		state = np.array(self._env.get_state())
		state = np.append(
			state[:2 + 2 * self._max_humans],
			state[102:102 + 2 * self._max_zombies]
		)
		state = np.vstack([state] * hyperparams.state_sequence_length)
		state = state[np.newaxis, ]

		return state

	def update_environment(self, action):
		# This must change if more action types are supported
		# if aciton < len(self._points):
		# 	self._env.update(points[action][0], points[action][1])
		# else:
		# 	self._env.update(self._env.shooter.x, self._env.shooter.y)
		self._env.update(self._points[action][0], self._points[action][1])

	def agent_observe(self, state, epsilon_decay=False):
		action = self._agent.get_action(state)
		self.update_environment(action)
		done = self._env.is_done()
		reward = self._env.reward
		new_state = self.get_state()

		self._agent.store_frame(
			state, action, reward, new_state, done
		)

		if epsilon_decay:
			self._agent.decay_epsilon()

		return new_state, done

	def train_agent(self, config=["experienced_replay", "infinite", "track"]):
		save_file = "-".join(config) + ".h5"
		self.initialize_agent()
		episode = 0

		self.initialize_environment()
		state = self.get_state()

		if "track" in config:
			avg_over = 100
			scores = collections.deque(maxlen=avg_over)
			averages = collections.deque(maxlen=avg_over)
			log_filename = "log-" + "-".join(config) + ".txt"

		if "experienced_replay" in config:
			if "infinite" in config:
				hyperparams.final_epsilon_frame = 10000000
				hyperparams.memory_size = 1000000
				hyperparams.replay_start_size = 50000

				while True:
					state, done = self.agent_observe(state, epsilon_decay=True)

					if self._render and episode % 20 == 0:
						self._renderer.draw_environment(self._env)
						time.sleep(self._render_delay)

					if done:
						episode += 1

						if "track" in config:
							scores.append(self._env.score)

							if episode >= avg_over:
								average = sum(np.array(scores))/avg_over
								averages.append(average)

							if episode % avg_over == 0:
								sys.stdout.write(
									"\repisode {}, average = {} - epsilon = {}"
									.format(
										episode, average, self._agent._epsilon
									)
								)
								sys.stdout.flush()

								with open(log_filename, "a") as log_file:
									log_file.write(
										",".join(map(str, averages)) + ","
									)

						self._agent.experienced_replay()
						self.initialize_environment()
						state = self.get_state()

						if episode % 100 == 0:
							self._agent.save_model(save_file)

			else:
				for episode in range(hyperparams.training_episodes):
					done = False
					while not done:
						state, done = self.agent_observe(state)

						if self._render and episode % 20 == 0:
							self._renderer.draw_environment(self._env)
							time.sleep(self._render_delay)


					if "track" in config:
						scores.append(self._env.score)

						if episode >= avg_over:
							average = sum(np.array(scores))/avg_over
							averages.append(average)

						if max(episode, 1) % avg_over == 0:
							sys.stdout.write(
								"\repisode {}, average = {} - epsilon = {}"
								.format(
									episode, average, self._agent._epsilon
								)
							)
							sys.stdout.flush()

							with open(log_filename, "a") as log_file:
								log_file.write(
									",".join(map(str, averages)) + ","
								)

					self._agent.experienced_replay()
					self._agent.decay_epsilon()
					self.initialize_environment()
					state = self.get_state()

					if episode % 100 == 0:
						self._agent.save_model(save_file)

		self._agent.save_model(save_file)
