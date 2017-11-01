import numpy as np, glob, os
from matplotlib import pyplot as plt

plot_type = "Nadam_check"
# plot_type = "networks"
# plot_type = "network_update"
# plot_type = "replay_sample"
# plot_type = "action"
try:
    os.mkdir("{}/plots".format(plot_type))
except FileExistsError:
    pass

def plot_save_multi(Y, title, item, x_axis='Score',
    x_start=None, x_end=None,
    name="test"):
    if x_start == None:
        x_start_tune = True
        x_start = np.finfo(float).max
    if x_end == None:
        x_end_tune = True
        x_end = np.finfo(float).min

    colors = ['red', 'green', 'blue', 'black']
    plt.figure()
    action_count = 0
    architectures = []
    for architecture in Y:
        if architecture in ["(1024, 512, 128, 128, 128, 64)", "(512, 512, 128, 128, 64, 8)"]:
            architectures.append(architecture)
            for i in range(len(Y[architecture])-1):
                architectures.append("")

            for action in Y[architecture]:
                x = np.array(Y[architecture][action][item])
                y = [action_count] * x.size
                plt.plot(x, y, color=colors[action_count % len(Y[architecture])], marker="o")

                if x_start_tune:
                    x_start = np.min([x.min(), x_start])
                if x_end_tune:
                    x_end = np.max([x.max(), x_end])

                action_count += 1

    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel("Architectures")
    plt.subplots_adjust(left=0.4)
    plt.yticks(range(len(architectures)*len(Y[architecture][action])), architectures)

    plt.axis([x_start, x_end, -1, action_count])
    plt.savefig(name, dpi=300)

def plot_save(Y, title, item, x_axis='Score',
    x_start=None, x_end=None,
    name="test"):
    if x_start == None:
        x_start_tune = True
        x_start = np.finfo(float).max
    if x_end == None:
        x_end_tune = True
        x_end = np.finfo(float).min

    for architecture in Y:
        x_start = np.finfo(float).max
        x_end = np.finfo(float).min
        plt.figure()
        action_count = 0
        for action in Y[architecture]:
            x = np.array(Y[architecture][action][item])
            y = [action_count] * x.size
            plt.plot(x, y, label=action, marker="o")

            if x_start_tune:
                x_start = np.min([x.min(), x_start])
            if x_end_tune:
                x_end = np.max([x.max(), x_end])

            action_count += 1

        plt.title(title + "\nfor {}".format(architecture))
        plt.xlabel(x_axis)
        plt.yticks([], [])

        plt.axis([x_start, x_end, -1, action_count])
        plt.legend()
        plt.savefig("{}_{}".format(name, architecture), dpi=300)

# files = glob.glob("./{}/*_check_log.txt".format(plot_type))
files = glob.glob("./{}/*.txt".format(plot_type))
# files = glob.glob("./{}/*.log".format(plot_type))

Y = {}
for filename in files:
    with open(filename, "r") as log_file:
        data = log_file.readlines()

    for d in data:
        # items = d.strip().split("_")
        # architecture = items[0]
        # action_type = " ".join(items[2:-2])
        # score = items[-2]
        # time = items[-1]
        architecture, action_type, score, time = d.strip().split("_")
        # architecture, _, action_type, score, time = d.strip().split("_")
        if architecture in Y:
            if action_type in Y[architecture]:
                Y[architecture][action_type]["score"].append(float(score))
                Y[architecture][action_type]["time"].append(float(time))
            else:
                Y[architecture][action_type] = {}
                Y[architecture][action_type]["score"] = [float(score)]
                Y[architecture][action_type]["time"] = [float(time)]
        else:
            Y[architecture] = {}
            Y[architecture][action_type] = {}
            Y[architecture][action_type]["score"] = [float(score)]
            Y[architecture][action_type]["time"] = [float(time)]

plot_save(Y, "Score Variation per Learning Rate", item="score", name="./{}/plots/score".format(plot_type))
plot_save(Y, "Time Variation per Learning Rate", item="time", x_axis='Time [s]', name="./{}/plots/time".format(plot_type))
plot_save_multi(Y, "Score Variation for Multiple Networks", item="score", name="./{}/plots/score_all".format(plot_type))
plot_save_multi(Y, "Time Variation for Multiple Networks", item="time", x_axis='Time [s]', name="./{}/plots/time_all".format(plot_type))
