import sys, hyperparmas, collections
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Nadam

class Agent:
	def __init__(self, state_dim, action_dim):
		self._memory = collections.deque(maxlen=hyperparmas.memory_size)
		self._epsilon = hyperparmas.initial_epsilon
		self._epsilon_decay = (
			(hyperparmas.initial_epsilon - hyperparmas.final_epsilon) /
			hyperparmas.final_epsilon_frame
		)
		self._model = self._compile_model(state_dim, action_dim)

	def _compile_model(self, state_dim, action_dim):
		model = Sequential()
		model.add(Dense(
			hyperparmas.hidden_layers[0],
			input_shape=(state_dim, hyperparmas.state_sequence_length),
			activation=hyperparmas.activation
		))

		for size in hyperparmas.hidden_layers[1:]:
			model.add(Dense(
				size,
				activation=hyperparmas.activation
			))

		model.add(Dense(action_dim, activation='linear'))
		model.compile(loss='mse', optimizer=Nadam(lr=hyperparmas.learning_rate))

		return model

	def _save_model(self, filename="keras_dqn.h5"):
		self._model.save(filename)
