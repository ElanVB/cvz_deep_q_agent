from interface import Interface
import numpy as np, time, sys, pickle, os

repetitions = 3
arch_index = int(sys.argv[1])
test_type = "replay_sample"
try:
    os.mkdir(test_type)
except FileExistsError:
    pass
save_file_name = test_type + "/log.txt"

def save_file(architecture, learning_rate, update, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}_{}\n".format(architecture, learning_rate, update, score, time_diff))

def train_and_test_agent(architecture, learning_rate, replay_type, memory_size, test_index):
	i = Interface(
		learning_rate=learning_rate,
		hidden_layers=architecture,
		max_humans=3, max_zombies=3,
        randomness=True, memory_size=memory_size
	)
	start = time.time()
	i.train_agent(
        save_file="{}/{}_{}_{}".format(test_type, architecture, replay_type, test_index),
		replay_type=replay_type, config=[
		"experienced_replay", "network_update_delay", "frame_skip", "log"
	])
	time_diff = time.time() - start
	score = i.test_agent()
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

for [replay_type, memory_size] in [["full", 3200], ["random", 10000]]:
    for index in range(repetitions):
        score, time_diff = train_and_test_agent(
    		architecture=architecture, learning_rate=lr,
            replay_type=replay_type, memory_size=memory_size, test_index=index
    	)
        save_file(architecture, lr, replay_type, score, time_diff)
