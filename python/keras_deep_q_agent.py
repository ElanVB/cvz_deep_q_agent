import sys, collections, random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import RMSprop
# from keras.optimizers import Nadam

class Agent:
	def __init__(
		self, state_dim, action_dim, initial_epsilon, final_epsilon,
		epsilon_decay, memory_size, learning_rate, gradient_momentum,
		squared_gradient_momentum, min_squared_gradient, state_sequence_length,
		activation, gamma, hidden_layers, batch_size, replay_start_size
	):
		self._epsilon = initial_epsilon
		self._final_epsilon = final_epsilon
		self._epsilon_decay = epsilon_decay
		self._state_dim = state_dim
		self._action_dim = action_dim
		self._model = self._compile_model(
			state_dim, action_dim, learning_rate, gradient_momentum,
			squared_gradient_momentum, min_squared_gradient,
			state_sequence_length, activation, hidden_layers
		)
		self._input_memory = collections.deque(maxlen=memory_size)
		self._target_memory = collections.deque(maxlen=memory_size)
		self._gamma = gamma
		self._batch_size = batch_size
		self._replay_start_size = replay_start_size

	def _compile_model(
		self, state_dim, action_dim, learning_rate, gradient_momentum,
		squared_gradient_momentum, min_squared_gradient, state_sequence_length,
		activation, hidden_layers
	):
		model = Sequential()
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
		model.compile(loss='mse', optimizer=RMSprop(lr=learning_rate))
		# model.compile(loss='mse', optimizer=Nadam(lr=learning_rate))

		return model

	def save_model(self, filename="keras_dqn.h5"):
		self._model.save(filename)

	def load_weights(self, filename="keras_dqn.h5"):
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
			target += (
				self._gamma *
				np.amax(self._model.predict(new_state)[0])
			)

		prev_target = self._model.predict(state)[0]
		new_target = prev_target
		new_target[action] = target

		self._input_memory.append(state[0])
		self._target_memory.append(new_target)

	def decay_epsilon(self):
		if self._epsilon > self._final_epsilon:
			self._epsilon -= self._epsilon_decay

	def experienced_replay(self, batches=1):
		if len(self._input_memory) >= self._batch_size and\
		len(self._input_memory) >= self._replay_start_size:
			# sample_indexes = np.random.choice(
			# 	len(self._memory), size=hyperparams.batch_size * batches
			# )
			# sample = collections.deque()
			# for sample_i in sample_indexes:
			# 	sample.append(self._memory[sample_i])
			#
			# # sample = np.array(self._memory)[sample_indexes]

			# sample_count = 0
			# for state, action, reward, new_state, done in self._memory:
			# # for state, action, reward, new_state, done in sample:
			# 	target = reward
			# 	if not done:
			# 		target += (
			# 			hyperparams.gamma *
			# 			np.amax(self._model.predict(new_state)[0])
			# 		)
			#
			# 	prev_target = self._model.predict(state)[0]
			# 	new_target = prev_target
			# 	new_target[action] = target
			#
			# 	inputs[sample_count] = state
			# 	targets[sample_count] = new_target
			# 	sample_count += 1
			self._model.fit(
				# self._input_memory, self._target_memory,
				np.array(self._input_memory), np.array(self._target_memory),
				batch_size=self._batch_size,
				epochs=1, verbose=0
				# , shuffle=False # slightly better result with 10-20s time increase
			)
