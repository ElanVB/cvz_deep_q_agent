from interface import Interface
import numpy as np, time, sys, pickle, os

repetitions = 3
arch_index = int(sys.argv[1])
test_type = "validation"
try:
    os.mkdir(test_type)
except FileExistsError:
    pass

save_file_name = test_type + "/validation_test_log.txt"

def save_file(architecture, learning_rate, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}\n".format(architecture, learning_rate, score, time_diff))

def train_and_test_agent(architecture, learning_rate, test_index):
	i = Interface(
		learning_rate=learning_rate,
		hidden_layers=architecture,
		max_humans=3, max_zombies=3,
        randomness=True
	)
	start = time.time()
	i.train_agent(
        save_file="{}/{}_{}".format(test_type, architecture, test_index),
        config=[
            "experienced_replay",
            "network_update_delay",
            # "target_network_update_delay"
            "frame_skip",
            "log"
	    ]
    )
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

for index in range(repetitions):
    score, time_diff = train_and_test_agent(
		architecture=architecture,
        learning_rate=lr,
        test_index=index
	)
    save_file(architecture, lr, score, time_diff)
