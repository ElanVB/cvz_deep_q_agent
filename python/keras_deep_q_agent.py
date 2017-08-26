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
