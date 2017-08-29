import sys, hyperparams, collections, random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Nadam

class Agent:
	def __init__(self, state_dim, action_dim):
		self._memory = collections.deque(maxlen=hyperparams.memory_size)
		self._epsilon = hyperparams.initial_epsilon
		self._epsilon_decay = (
			(hyperparams.initial_epsilon - hyperparams.final_epsilon) /
			hyperparams.final_epsilon_episode
			# hyperparams.final_epsilon_frame
		)
		self._state_dim = state_dim
		self._action_dim = action_dim
		self._model = self._compile_model(state_dim, action_dim)

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
		self._memory.append((state, action, reward, new_state, done))

	def decay_epsilon(self):
		if self._epsilon > hyperparams.final_epsilon:
			self._epsilon -= self._epsilon_decay

	def experienced_replay(self):
		if len(self._memory) > hyperparams.batch_size and\
		len(self._memory) > hyperparams.replay_start_size:
			inputs = np.zeros((
				hyperparams.batch_size,
				hyperparams.state_sequence_length,
				self._state_dim
			))
			targets = np.zeros((
				hyperparams.batch_size,
				self._action_dim
			))
			sample = random.sample(self._memory, hyperparams.batch_size)

			sample_count = 0
			for state, action, reward, new_state, done in sample:
				target = reward
				if not done:
					target += (
						hyperparams.gamma *
						np.amax(self._model.predict(new_state)[0])
					)

				prev_target = self._model.predict(state)[0]
				new_target = prev_target
				new_target[action] = target

				inputs[sample_count] = state
				targets[sample_count] = new_target
				sample_count += 1

			self._model.fit(
				inputs, targets,
				batch_size=hyperparams.batch_size,
				epochs=1, verbose=0
			)
