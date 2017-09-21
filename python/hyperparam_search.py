from interface import Interface
import numpy as np, time

learning_rate_scans = 3
learning_rate_segments = 5 + 2
max_params = 1e6
architecture_checks = 20
layer_sizes = (8, 16, 32, 64, 128, 256, 512, 1024)
save_file_name = "hyperparam_search_log.txt"

open(save_file_name, "w").close()

def save_file(architecture, learning_rate, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}\n".format(architecture, learning_rate, score, time_diff))

def paramaters(layers):
	return np.prod(layers)

def train_and_test_agent(architecture, learning_rate):
	start = time.time()
	time.sleep(np.random.rand() * 0.05)
	i = Interface(
		learning_rate=learning_rate,
		# state_sequence_length=hyperparams.state_sequence_length,
		hidden_layers=architecture,
		max_humans=1, max_zombies=1
	)
	i.train_agent(config=[
		"experienced_replay", "experimental_network_update_delay", "frame_skip"
	])
	score = i.test_agent()
	time_diff = time.time() - start
	return score, time_diff

architectures = []
for i in range(architecture_checks):
	size = np.random.randint(1, 7)
	architecture = []
	for j in range(size):
		architecture.append(np.random.choice(layer_sizes))
	architecture.sort(reverse=True)
	architectures.append(tuple(architecture))

architectures = list(set(architectures))
architectures.sort(key=lambda x: paramaters(x))

for architecture in architectures:
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
