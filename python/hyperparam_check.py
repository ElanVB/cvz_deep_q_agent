from interface import Interface
import numpy as np, time, sys, pickle, os

repetitions = 3
optimizer = sys.argv[1]
arch_index = int(sys.argv[2])
save_file_name = "{}_hyperparam_check_log.txt".format(optimizer)

def save_file(architecture, learning_rate, score, time_diff):
	with open(save_file_name, "a") as f:
		f.write("{}_{}_{}_{}\n".format(architecture, learning_rate, score, time_diff))

def train_and_test_agent(architecture, learning_rate):
	i = Interface(
		optimizer=optimizer,
		learning_rate=learning_rate,
		hidden_layers=architecture,
		max_humans=3, max_zombies=3
	)
	start = time.time()
	i.train_agent(save_file="{}.h5".format(optimizer), config=[
		"experienced_replay", "experimental_network_update_delay", "frame_skip"
	])
	time_diff = time.time() - start
	score = i.test_agent()
	return score, time_diff

data = {}

if not os.path.isfile("{}_parsed_hyperparam.txt".format(optimizer)):
    arch_count = -1
    prev_arch = (1,)

    with open("{}_hyperparam_search_log.txt".format(optimizer), "r") as data_file:
        lines = data_file.readlines()
        for line in lines:
            arch, lr, score, time = line.strip().split("_")
            arch = tuple([
                int(x) for x in
                arch.replace("(", "").replace(")", "").split(",")
                if x != ""
            ])
            lr = float(lr)
            score = float(score)
            time = float(time)

            if prev_arch != arch:
                prev_arch = arch
                arch_count += 1
                data[arch_count] = []

            data[arch_count].append({
                "arch": arch,
                "lr": lr,
                "score": score,
                "time": time
            })

    with open("{}_parsed_hyperparam.txt".format(optimizer), "wb") as pickle_file:
        pickle.dump(data, pickle_file)
else:
    with open("{}_parsed_hyperparam.txt".format(optimizer), "rb") as pickle_file:
        data = pickle.load(pickle_file)

arch_data = data[arch_index]
arch_data.sort(key=lambda x: x["score"]/x["time"], reverse=True)
top_arch_data = arch_data[:3]

for entry in top_arch_data:
    architecture = entry["arch"]
    lr = entry["lr"]
    for _ in range(repetitions):
        score, time_diff = train_and_test_agent(
    		architecture=architecture, learning_rate=lr
    	)
        save_file(architecture, lr, score, time_diff)
