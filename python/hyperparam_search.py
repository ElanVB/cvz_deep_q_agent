# from interface import Interface
import numpy as np

learning_rate_scans = 3
learning_rate_segments = 5
learning_rates = [10 ** -i for i in range(1, 8)]
max_params = 1e6
architecture_checks = 20
layer_sizes = (8, 16, 32, 64, 128, 256, 512, 1024)
