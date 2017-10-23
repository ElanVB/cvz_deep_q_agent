from interface import Interface
import numpy as np, time, sys, pickle, os

repetitions = 1
arch_index = int(sys.argv[1])
test_type = "state_dim"
try:
    os.mkdir(test_type)
except FileExistsError:
    pass
save_file_name = test_type + "/state_dim_test_log.txt"

def save_file(architecture, learning_rate, dim, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}_{}\n".format(architecture, learning_rate, dim, score, time_diff))

def train_and_test_agent(architecture, learning_rate, dim, test_index):
	i = Interface(
		learning_rate=learning_rate,
		hidden_layers=architecture,
		max_humans=dim, max_zombies=dim,
        randomness=True
	)
	start = time.time()
	i.train_agent(
        num_humans=1, num_zombies=1,
        save_file="{}/{}_{}_{}".format(test_type, architecture, dim, test_index),
		config=[
		"experienced_replay", "network_update_delay", "frame_skip", "log"
	])
	time_diff = time.time() - start
	score = i.test_agent(num_humans=1, num_zombies=1)
	return score, time_diff

networks = []

if not os.path.isfile("parsed_networks.txt"):
    with open("test_networks.txt", "r") as network_file:
        lines = network_file.readlines()
        for line in lines:
            arch, lr = line.strip().split("_")
            arch = tuple([
                int(x) for x in
                arch.replace("(", "").replace(")", "").split(",")
                if x != ""
            ])
            lr = float(lr)

            networks.append({
                "arch": arch,
                "lr": lr
            })

    with open("parsed_networks.txt", "wb") as pickle_file:
        pickle.dump(networks, pickle_file)
else:
    with open("parsed_networks.txt", "rb") as pickle_file:
        networks = pickle.load(pickle_file)

network = networks[arch_index]
architecture = network["arch"]
lr = network["lr"]

for dim in [1, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99]:
    for index in range(repetitions):
        score, time_diff = train_and_test_agent(
    		architecture=architecture, learning_rate=lr, dim=dim, test_index=index
    	)
        save_file(architecture, lr, dim, score, time_diff)
