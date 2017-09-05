import sys, hyperparams, collections, random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Nadam

class Agent:
	def __init__(self, state_dim, action_dim):
		self._epsilon = hyperparams.initial_epsilon
		self._epsilon_decay = (
			(hyperparams.initial_epsilon - hyperparams.final_epsilon) /
			hyperparams.final_epsilon_episode
			# hyperparams.final_epsilon_frame
		)
		self._state_dim = state_dim
		self._action_dim = action_dim
		self._model = self._compile_model(state_dim, action_dim)

		# self._memory = collections.deque(maxlen=hyperparams.memory_size)
		self._input_memory = collections.deque(maxlen=hyperparams.memory_size)
		self._target_memory = collections.deque(maxlen=hyperparams.memory_size)

		# self._input_memory = np.zeros((
		# 	hyperparams.batch_size * hyperparams.network_update_frequency,
		# 	hyperparams.state_sequence_length,
		# 	self._state_dim
		# ))
		# self._target_memory = np.zeros((
		# 	hyperparams.batch_size * hyperparams.network_update_frequency,
		# 	self._action_dim
		# ))
		# self._memory_count = 0

	def _compile_model(self, state_dim, action_dim):
		model = Sequential()
		model.add(Dense(
			hyperparams.hidden_layers[0],
			input_shape=(hyperparams.state_sequence_length, state_dim),
			activation=hyperparams.activation
		))
		model.add(Flatten())

		for size in hyperparams.hidden_layers[1:]:
			model.add(Dense(
				size,
				activation=hyperparams.activation
			))

		model.add(Dense(action_dim, activation='linear'))
		model.compile(loss='mse', optimizer=Nadam(lr=hyperparams.learning_rate))

		return model

	def save_model(self, filename="keras_dqn.h5"):
		self._model.save(filename)

	def load_weights(self, filename="keras_dqn.h5"):
		self._model.load_weights(filename)

	def get_action(self, state, on_policy=False):
		if not on_policy and np.random.rand() <= self._epsilon:
			return int(np.random.rand() * self._action_dim)
		else:
			return np.argmax(self._model.predict(state)[0])

	def store_frame(self, state, action, reward, new_state, done):
		target = reward
		if not done:
			target += (
				hyperparams.gamma *
				np.amax(self._model.predict(new_state)[0])
			)

		prev_target = self._model.predict(state)[0]
		new_target = prev_target
		new_target[action] = target

		# self._input_memory[self._memory_count] = state[0]
		# self._target_memory[self._memory_count] = new_target
		# self._memory_count += 1
		# if self._memory_count >= self._input_memory.shape[0]:
		# 	self._memory_count = 0

		self._input_memory.append(state[0])
		self._target_memory.append(new_target)
		# self._memory.append((state, action, reward, new_state, done))

	def decay_epsilon(self):
		if self._epsilon > hyperparams.final_epsilon:
			self._epsilon -= self._epsilon_decay

	def experienced_replay(self, batches=1):
		if len(self._input_memory) >= hyperparams.batch_size and\
		len(self._input_memory) >= hyperparams.replay_start_size:
			# inputs = np.zeros((
			# 	hyperparams.batch_size * batches,
			# 	hyperparams.state_sequence_length,
			# 	self._state_dim
			# ))
			# targets = np.zeros((
			# 	hyperparams.batch_size * batches,
			# 	self._action_dim
			# ))

			# # sample = random.sample(
			# # 	self._memory, hyperparams.batch_size * batches
			# # )
			#
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
				batch_size=hyperparams.batch_size,
				epochs=1, verbose=0
				# , shuffle=False # slightly better result with 10-20s time increase
			)
