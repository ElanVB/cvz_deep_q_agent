import numpy as np, glob, os
from matplotlib import pyplot as plt

# plot_type = "networks"
plot_type = "validation_large_sample"
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

    plt.figure()

    data = []
    architectures = []
    for architecture in Y:
        architectures.append(architecture)
        data.append(Y[architecture][item])

    plt.barh(range(len(architectures)), data)

    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel("Architectures")
    plt.subplots_adjust(left=0.4)
    plt.yticks(range(len(architectures)), architectures)

    plt.savefig(name, dpi=300)

files = glob.glob("./{}/*.txt".format(plot_type))
# files = glob.glob("./{}/*.log".format(plot_type))

Y = {}
for filename in files:
    with open(filename, "r") as log_file:
        data = log_file.readlines()

    for d in data:
        architecture, _, score, time = d.strip().split("_")
        if architecture in Y:
            Y[architecture]["score"].append(float(score))
            Y[architecture]["time"].append(float(time))
        else:
            Y[architecture] = {}
            Y[architecture]["score"] = [float(score)]
            Y[architecture]["time"] = [float(time)]

for architecture in Y:
    Y[architecture]["score"] = np.mean(np.array(Y[architecture]["score"]))
    Y[architecture]["time"] = np.mean(np.array(Y[architecture]["time"]))
    Y[architecture]["s/t"] = Y[architecture]["score"] / Y[architecture]["time"]

plot_save_multi(Y, "Score per Architecture", item="score", name="./{}/plots/score".format(plot_type))
plot_save_multi(Y, "Time per Architecture", item="time", x_axis='Time [s]', name="./{}/plots/time".format(plot_type))
plot_save_multi(Y, "Score/Time per Architecture", item="s/t", x_axis='Score/Time [p/s]', name="./{}/plots/score_time".format(plot_type))
