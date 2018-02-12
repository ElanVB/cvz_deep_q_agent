import sys, collections, random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D
from keras.optimizers import RMSprop, Nadam, Adam

class Agent:
	def __init__(
		self, state_dim, action_dim, initial_epsilon, final_epsilon,
		epsilon_decay, memory_size, optimizer, learning_rate, gradient_momentum,
		squared_gradient_momentum, min_squared_gradient, state_sequence_length,
		activation, gamma, hidden_layers, batch_size, replay_start_size,
		network_type="DQ", state_shape=None
	):
		self._epsilon = initial_epsilon
		self._final_epsilon = final_epsilon
		self._epsilon_decay = epsilon_decay
		self._state_dim = state_dim
		self._action_dim = action_dim
		self._network_type = network_type
		self._model = self._compile_model(
			state_dim, action_dim, optimizer, learning_rate, gradient_momentum,
			squared_gradient_momentum, min_squared_gradient,
			state_sequence_length, activation, hidden_layers, state_shape
		)
		if network_type == "DDQ":
			self._target_model = self._compile_model(
				state_dim, action_dim, optimizer, learning_rate, gradient_momentum,
				squared_gradient_momentum, min_squared_gradient,
				state_sequence_length, activation, hidden_layers, state_shape
			)
		self._input_memory = collections.deque(maxlen=memory_size)
		self._target_memory = collections.deque(maxlen=memory_size)
		self._gamma = gamma
		self._batch_size = batch_size
		self._replay_start_size = replay_start_size

	def _compile_model(
		self, state_dim, action_dim, optimizer, learning_rate,
		gradient_momentum, squared_gradient_momentum, min_squared_gradient,
		state_sequence_length, activation, hidden_layers, state_shape=None
	):
		model = Sequential()
		if state_shape != None:
			model.add(Conv2D(16, (3, 3), activation="relu", input_shape=(state_shape + (1,))))
			model.add(Conv2D(32, (3, 3), activation="relu"))
			# model.add(Dense(
			# 	hidden_layers[0],
			# 	input_shape=state_shape, # can think about how to add multiple frames, but not needed for now
			# 	activation=activation
			# ))
		else:
			model.add(Dense(
				hidden_layers[0],
				input_shape=(state_sequence_length, state_dim),
				activation=activation
			))
		model.add(Flatten())

		for size in hidden_layers[1:]:
			model.add(Dense(
				size,
				activation=activation
			))

		model.add(Dense(action_dim, activation='linear'))

		if optimizer == "RMSprop":
			optimizer = RMSprop(lr=learning_rate)
		elif optimizer == "Adam":
			optimizer = Adam(lr=learning_rate)
		elif optimizer == "Nadam":
			optimizer = Nadam(lr=learning_rate)
		else:
			raise ValueError("optimizer not supported")

		model.compile(loss='mse', optimizer=optimizer)

		return model

	def save_model(self, filename="keras_dqn.h5"):
		if ".h5" not in filename:
			filename += ".h5"
		self._model.save(filename)

	def load_weights(self, filename="keras_dqn.h5"):
		if ".h5" not in filename:
			filename += ".h5"
		self._model.load_weights(filename)

	def get_action(self, state, on_policy=False):
		if not on_policy and np.random.rand() <= self._epsilon:
			return np.random.randint(self._action_dim)
			# return int(np.random.rand() * self._action_dim)
		else:
			return np.argmax(self._model.predict(state)[0])

	def store_frame(self, state, action, reward, new_state, done):
		target = reward
		if not done:
			if self._network_type == "DQ":
				target += (
					self._gamma *
					np.amax(self._model.predict(new_state)[0])
				)
			elif self._network_type == "DDQ":
				target += (
					self._gamma *
					self._target_model.predict(new_state)[0][np.argmax(self._model.predict(new_state)[0])]
				)
			else:
				raise ValueError("given train_type not supported.")

		if self._network_type == "DQ":
			prev_target = self._model.predict(state)[0]
		elif self._network_type == "DDQ":
			prev_target = self._target_model.predict(state)[0]

		new_target = prev_target
		new_target[action] = target

		self._input_memory.append(state[0])
		self._target_memory.append(new_target)

	def decay_epsilon(self):
		if self._epsilon > self._final_epsilon:
			self._epsilon -= self._epsilon_decay

	def experienced_replay(self, batches=1, replay_type="full"):
		if len(self._input_memory) >= self._batch_size and\
		len(self._input_memory) >= self._replay_start_size:
			if replay_type == "random":
				sample_indexes = np.random.choice(
					len(self._input_memory), size=self._batch_size*batches
				)
				inputs = np.array(self._input_memory)[sample_indexes]
				targets = np.array(self._target_memory)[sample_indexes]
			elif replay_type == "truncated":
				inputs = np.array(self._input_memory)[-batches*self._batch_size:]
				targets = np.array(self._target_memory)[-batches*self._batch_size:]
			elif replay_type == "full":
				inputs = np.array(self._input_memory)
				targets = np.array(self._target_memory)
			else:
				raise ValueError("invaild replay type")

			if self._network_type == "DQ":
				self._model.fit(
					inputs, targets,
					batch_size=self._batch_size,
					epochs=1, verbose=0
					# , shuffle=False # slightly better result with 10-20s time increase
				)
			elif self._network_type == "DDQ":
				self._target_model.fit(
					inputs, targets,
					batch_size=self._batch_size,
					epochs=1, verbose=0
					# , shuffle=False # slightly better result with 10-20s time increase
				)
			else:
				raise ValueError("invaild network type")

	def update_prediction_network(self):
		self._target_model.save("temp")
		self._model.load_weights("temp")
