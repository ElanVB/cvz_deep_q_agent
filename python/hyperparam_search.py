from interface import Interface
import numpy as np, time, sys

learning_rate_scans = 3
learning_rate_segments = 5 + 2
max_params = 1e6
architecture_checks = 20
layer_sizes = (8, 16, 32, 64, 128, 256, 512, 1024)
optimizer = sys.argv[1]
architecture_index = int(sys.argv[2])
save_file_name = "{}_hyperparam_search_log.txt".format(optimizer)

# open(save_file_name, "w").close()

def save_file(architecture, learning_rate, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}\n".format(architecture, learning_rate, score, time_diff))

def paramaters(layers):
	return np.prod(layers)

def train_and_test_agent(architecture, learning_rate):
	i = Interface(
		optimizer=optimizer,
		learning_rate=learning_rate,
		# state_sequence_length=hyperparams.state_sequence_length,
		hidden_layers=architecture,
		max_humans=1, max_zombies=1
	)
	start = time.time()
	i.train_agent(save_file="{}.h5".format(optimizer), config=[
		"experienced_replay", "experimental_network_update_delay", "frame_skip"
	])
	time_diff = time.time() - start
	score = i.test_agent()
	return score, time_diff

architectures = [
	(8,), (16,), (1024,), (512, 64), (256, 32, 16), (128, 64, 32),
	(1024, 64, 32), (256, 64, 32, 8, 8), (1024, 512, 16, 16),
	(512, 256, 32, 32), (1024, 512, 128, 8), (512, 64, 64, 32, 32),
	(512, 512, 256, 64), (512, 256, 256, 64, 16), (1024, 256, 256, 32, 16, 16),
	(512, 512, 128, 128, 64, 8), (1024, 512, 128, 128, 128, 64)
]
# for i in range(architecture_checks):
# 	size = np.random.randint(1, 7)
# 	architecture = []
# 	for j in range(size):
# 		architecture.append(np.random.choice(layer_sizes))
# 	architecture.sort(reverse=True)
# 	architectures.append(tuple(architecture))
#
# architectures = list(set(architectures))
# architectures.sort(key=lambda x: paramaters(x))

# for architecture in architectures:
architecture = architectures[architecture_index]

scores = np.array([])
learning_rates = np.array([10 ** -i for i in range(1, 8)])

for lr in learning_rates:
	score, time_diff = train_and_test_agent(
		architecture=architecture, learning_rate=lr
	)
	scores = np.append(scores, score)

	save_file(architecture, lr, score, time_diff)
	print(
		"{} - lr: {:.7f} => score: {:.3f}, time: {:.2f}"
		.format(architecture, lr, score, time_diff)
	)

top_2 = np.argsort(scores)[-2:]
learning_rates = learning_rates[top_2]
scores = scores[top_2]
top_2 = np.argsort(scores)[-2:]

for seg in range(learning_rate_scans):
	for lr in np.logspace(
		np.log10(learning_rates[top_2[0]]),
		np.log10(learning_rates[top_2[1]]),
		learning_rate_segments,
		endpoint=True
	)[1:-1]:
		learning_rates = np.append(learning_rates, lr)
		score, time_diff = train_and_test_agent(
			architecture=architecture, learning_rate=lr
		)
		scores = np.append(scores, score)

		save_file(architecture, lr, score, time_diff)
		print(
			"{} - lr: {:.7f} => score: {:.3f}, time: {:.2f}"
			.format(architecture, lr, score, time_diff)
		)

	top_2 = np.argsort(scores)[-2:]
