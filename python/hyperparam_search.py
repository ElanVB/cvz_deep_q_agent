# from interface import Interface
import numpy as np

learning_rate_scans = 3
learning_rate_segments = 5
learning_rates = [10 ** -i for i in range(1, 8)]
max_params = 1e6
architecture_checks = 20
layer_sizes = (8, 16, 32, 64, 128, 256, 512, 1024)

architectures = []
for i in range(architecture_checks):
	size = np.random.randint(1, 9)
	architecture = []
	for j in range(size):
		architecture.append(np.random.choice(layer_sizes))
	architecture.sort(reverse=True)
	architectures.append(tuple(architecture))

architectures = list(set(architectures))
architectures.sort(key=lambda x: len(x))

# for each achitecture
#	for each learning_rate
#		create an agent, train it, store the test score
#	for learning_rate_scans
#		find the rates that got the best 2 scores
#		divide the space between the rates linearly in learning_rate_segments
#		for each learning_rate
# 			create an agent, train it, store the test score
# print the best leraning_rate and score
#### write all of this to a file as you go ####

# i = Interface(
# 	learning_rate=hyperparams.learning_rate,
# 	state_sequence_length=hyperparams.state_sequence_length,
# 	hidden_layers=hyperparams.hidden_layers,
# 	max_humans=1, max_zombies=1
# )
# i.train_agent(config=[
# 	"experienced_replay", "experimental_network_update_delay", "frame_skip"
# ])
# i.test_agent()
