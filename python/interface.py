import sys, time, random, collections, hyperparams
import numpy as np
from environment import Environment
from renderer import Renderer
from keras_deep_q_agent import Agent

class Interface:
	def __init__(
		self, training_episodes=hyperparams.training_episodes,
		frame_skip_rate=hyperparams.frame_skip_rate,
		initial_epsilon=hyperparams.initial_epsilon,
		final_epsilon=hyperparams.final_epsilon,
		epsilon_decay=hyperparams.epsilon_decay,
		memory_size=hyperparams.memory_size,
		optimizer=hyperparams.optimizer,
		learning_rate=hyperparams.learning_rate,
		gradient_momentum=hyperparams.gradient_momentum,
		squared_gradient_momentum=hyperparams.squared_gradient_momentum,
		min_squared_gradient=hyperparams.min_squared_gradient,
		state_sequence_length=hyperparams.state_sequence_length,
		activation=hyperparams.activation,
		gamma=hyperparams.gamma,
		hidden_layers=hyperparams.hidden_layers,
		batch_size=hyperparams.batch_size,
		replay_start_size=hyperparams.replay_start_size,
		test_episodes=hyperparams.test_episodes,
		validate_episodes=hyperparams.validate_episodes,
		network_update_frequency=hyperparams.network_update_frequency,
		render=False, render_delay=0.03, max_humans=1, max_zombies=1,
		randomness=False, fine_tune=False, actions="default", environment=None
	):
		self._state_sequence_length = state_sequence_length
		self._training_episodes = training_episodes
		self._network_update_frequency = network_update_frequency
		self._frame_skip_rate = frame_skip_rate
		self._test_episodes = test_episodes
		self._validate_episodes = validate_episodes

		self._initial_epsilon = initial_epsilon
		self._final_epsilon = final_epsilon
		self._epsilon_decay = epsilon_decay
		self._memory_size = memory_size
		self._optimizer = optimizer
		self._learning_rate = learning_rate
		self._gradient_momentum = gradient_momentum
		self._squared_gradient_momentum = squared_gradient_momentum
		self._min_squared_gradient = min_squared_gradient
		self._activation = activation
		self._gamma = gamma
		self._hidden_layers = hidden_layers
		self._batch_size = batch_size
		self._replay_start_size = replay_start_size

		self._render = render
		self._render_delay = render_delay
		if render:
			self._renderer = Renderer()

		self._max_humans = max_humans
		self._max_zombies = max_zombies

		self._input_dim = 2 + 2*max_humans + 2*max_zombies

		if actions == "default":
			self._points = [(0, 0), (16000, 0), (0, 9000), (16000, 9000)]
			self._output_dim = len(self._points)
		elif actions == "default+static":
			self._points = [(0, 0), (16000, 0), (0, 9000), (16000, 9000)]
			self._output_dim = len(self._points)+1 # plus one for no-op
		elif actions == "larger":
			self._points = [
				(0, 0), (0, 4500), (16000, 0), (8000, 0), (8000, 9000),
				(0, 9000), (16000, 4500), (16000, 9000)
			]
			self._output_dim = len(self._points)
		elif actions == "larger+static":
			self._points = [
				(0, 0), (0, 4500), (16000, 0), (8000, 0), (8000, 9000),
				(0, 9000), (16000, 4500), (16000, 9000)
			]
			self._output_dim = len(self._points)+1 # plus one for no-op
		else:
			raise ValueError("action value not supported")

		self._randomness = randomness
		self._fine_tune = fine_tune
		self._env = Environment(0, 0, better_rewards=True)

		self._environment = self._env.parse_state_file(environment)\
		if environment != None else None

	def initialize_agent(self, weights=None):
		self._agent = Agent(
			state_dim=self._input_dim, action_dim=self._output_dim,
			initial_epsilon=self._initial_epsilon,
			final_epsilon=self._final_epsilon,
			epsilon_decay=self._epsilon_decay, memory_size=self._memory_size,
			optimizer=self._optimizer,
			learning_rate=self._learning_rate,
			gradient_momentum=self._gradient_momentum,
			squared_gradient_momentum=self._squared_gradient_momentum,
			min_squared_gradient=self._min_squared_gradient,
			state_sequence_length=self._state_sequence_length,
			activation=self._activation, gamma=self._gamma,
			hidden_layers=self._hidden_layers, batch_size=self._batch_size,
			replay_start_size=self._replay_start_size
		)

		if weights != None:
			if not isinstance(weights, str):
				raise TypeError(
					"weights must be a string path to your weights file"
				)

			self._agent.load_weights(weights)

	def initialize_environment(
		self, num_humans=None, num_zombies=None, randomness=True
	):
		if num_humans == None:
			num_humans = self._max_humans

		if num_zombies == None:
			num_zombies = self._max_zombies

		if self._environment != None:
			self._env.load_state(self._environment)
		else:
			if randomness and self._randomness:
				humans = random.randrange(1, num_humans+1)
				zombies = random.randrange(1, num_zombies+1)
			else:
				humans = num_humans
				zombies = num_zombies

			self._env.reset(humans, zombies)

	def get_state(self):
		state = np.array(self._env.get_state())
		state = np.append(
			state[:(2 + 2 * self._max_humans)],
			state[200:(200 + 2 * self._max_zombies)]
		)
		return state

	def get_state_sequence(self, previous_sequence=None):
		state = self.get_state()

		if previous_sequence is None:
			state = np.vstack([state] * self._state_sequence_length)
		else:
			state = np.vstack([
				state,
				previous_sequence[0][:self._state_sequence_length-1]
			])

		state = state[np.newaxis, ]
		return state

	def update_environment(self, action):
		# This must change if more action types are supported
		if action < len(self._points):
			self._env.update(self._points[action][0], self._points[action][1])
		else:
			self._env.update(self._env.shooter.x, self._env.shooter.y)
		# self._env.update(self._points[action][0], self._points[action][1])

	def agent_observe(
		self, state, epsilon_decay=False, use_previous_action=False
	):
		if not use_previous_action:
			action = self._agent.get_action(state)
			self._previous_action = action

		self.update_environment(self._previous_action)
		done = self._env.is_done()
		reward = self._env.reward
		new_state = self.get_state_sequence(state)

		self._agent.store_frame(
			state, self._previous_action, reward, new_state, done
		)

		if epsilon_decay:
			self._agent.decay_epsilon()

		return new_state, done

	def agent_on_policy_act(self, state):
		action = self._agent.get_action(state, on_policy=True)
		self.update_environment(action)
		done = self._env.is_done()
		new_state = self.get_state_sequence(state)

		return new_state, done

	def log(self, filename, data):
	    filename += ".log"
	    with open(filename, "a") as log_file:
	        log_file.write(",".join(map(str, data)) + ",")

	def print_update(self, episode, validation_score):
	    sys.stdout.write(
	        "\repisode {}, val = {:.4f}, eps = {:.4f}"
	            .format(episode, validation_score, self._agent._epsilon)
	    )
	    sys.stdout.flush()

	def frame_skip_observe(self, current_frame, state):
	    if current_frame % self._frame_skip_rate == 0:
	        state, done = self.agent_observe(state)
	    else:
	        state, done = self.agent_observe(state, use_previous_action=True)

	    current_frame += 1

	    return state, done, current_frame

	def render(self):
	    self._renderer.draw_environment(self._env)
	    time.sleep(self._render_delay)

	def reset_episode(self, num_humans, num_zombies, randomness=True):
	    randomness = randomness and self._randomness
	    self.initialize_environment(num_humans, num_zombies, randomness)
	    state = self.get_state_sequence()
	    current_frame = 0
	    return state, current_frame

	def play_episode(self, num_humans, num_zombies, frame_skip=True, experienced_replay=True, replay_batches=1):
	    state, current_frame = self.reset_episode(num_humans, num_zombies)
	    done = False

	    while not done:
	        if frame_skip:
	            state, done, current_frame =\
	                self.frame_skip_observe(current_frame, state)
	        else:
	            state, done = self.agent_observe(state)

	    self._agent.decay_epsilon()
	    if experienced_replay:
	        self._agent.experienced_replay(replay_batches)

	def check_point(self, episode, num_humans, num_zombies, save_file, log=False):
	    validation_score =\
	        self.test_agent(num_humans, num_zombies, validate=True)
	    self.print_update(episode, validation_score)
	    self._agent.save_model(save_file)
	    if log:
	        self.log(save_file, [validation_score])

	def train_agent(
	    self, save_file=None, weights=None, num_humans=None, num_zombies=None,
	    config=[
	        "experienced_replay", "infinite", "log", "frame_skip",
	        "experimental_network_update_delay"
	    ]
	):
	    if save_file == None:
	        save_file = "-".join(config)

	    self.initialize_agent(weights)

	    if "experimental_network_update_delay" in config:
	        for episode in range(
	            self._training_episodes // self._network_update_frequency
	        ):
	            for observation in range(self._network_update_frequency):
	                self.play_episode(
						num_humans, num_zombies, "frame_skip" in config,
	                    experienced_replay=(observation+1 == self._network_update_frequency),
	                    replay_batches=self._network_update_frequency
	                )

	            self.check_point(
	                (episode+1)*self._network_update_frequency,
	                num_humans, num_zombies, save_file, log=("log" in config)
	            )
	    elif "experienced_replay" in config:
	        if "infinite" in config:
	            episode = 0
	            while True:
	                self.play_episode(num_humans, num_zombies, "frame_skip" in config)

	                episode += 1
	                if episode % 100 == 0:
	                    self.check_point(
	                        episode, num_humans, num_zombies, save_file,
	                        log=("log" in config)
	                    )
	        else:
	            for episode in range(self._training_episodes):
	                self.play_episode(num_humans, num_zombies, "frame_skip" in config)

	                if episode % 100 == 0:
	                    self.check_point(
	                        episode, num_humans, num_zombies, save_file,
	                        log=("log" in config)
	                    )
	    else:
	        raise ValueError("config is not valid")

	    self.check_point(
	        "FINAL", num_humans, num_zombies, save_file,
	        log=("log" in config)
	    )

	def test_agent(self, num_humans=None, num_zombies=None, validate=False):
		total_score = 0.0
		end_episode = self._validate_episodes if validate else self._test_episodes

		for episode in range(end_episode):
			state, _ = self.reset_episode(num_humans, num_zombies, randomness=False)
			done = False

			while not done:
				state, done = self.agent_on_policy_act(state)

				if self._render and validate and episode+1 == end_episode:
					self.render()

			total_score += self._env.score

		average_score = total_score/end_episode
		return average_score

	def demo_agent(self, episodes=10, infinite=False, num_humans=None, num_zombies=None):
		total_score = 0.0
		renderer = Renderer(window_scale=.75)

		if infinite:
			episodes = np.iinfo(np.int32).max

		for episode in range(episodes):
			self.initialize_environment(num_humans, num_zombies)
			state = self.get_state_sequence()
			done = False
			reward = 0

			while not done:
				state, done = self.agent_on_policy_act(state)
				reward += self._env.reward
				renderer.draw_environment(self._env)
				time.sleep(self._render_delay)

			total_score += self._env.score

			sys.stdout.write(
				"\rscore = {:4d}, reward = {:3.2f}"
				.format(self._env.score, reward)
			)
			sys.stdout.flush()
			time.sleep(1)

		print(
			"\nAverage score: {}".format(total_score/episodes)
		)
