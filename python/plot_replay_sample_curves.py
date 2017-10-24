import numpy as np, glob, os
from matplotlib import pyplot as plt

# plot_type = "replay_sample"
plot_type = "network_update"
try:
    os.mkdir("{}/plots".format(plot_type))
except FileExistsError:
    pass

def plot_save(x, y, title, x_axis='Episode', y_axis='Score',
    x_start=None, x_end=None, y_start=None, y_end=None,
    name="test"):
    if ".png" not in name:
        name += ".png"
    if x_start == None:
        x_start = x.min()
    if x_end == None:
        x_end = x.max()
    if y_start == None:
        y_start = y.min()
    if y_end == None:
        y_end = y.max()

    plt.figure()

    plt.plot(x, y, color="blue")
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.axis([x_start, x_end, y_start, y_end])
    plt.savefig(name, dpi=300)

def plot_save_multi(Y, title, random=None, approx_optimal=None, x_axis='Episode', y_axis='Score',
    x_start=None, x_end=None, y_start=None, y_end=None,
    name="test"):
    if ".png" not in name:
        name += ".png"
    if x_start == None:
        x_start_tune = True
        x_start = np.finfo(float).max
    if x_end == None:
        x_end_tune = True
        x_end = np.finfo(float).min
    if y_start == None:
        y_start_tune = True
        y_start = np.finfo(float).max
    if y_end == None:
        y_end_tune = True
        y_end = np.finfo(float).min

    plt.figure(figsize=(7, 4))

    for replay in Y:
        y = Y[replay]["data"]
        x = Y[replay]["x"]
        plt.plot(x, y, label=replay)

        if x_start_tune:
            x_start = np.min([x.min(), x_start])
        if x_end_tune:
            x_end = np.max([x.max(), x_end])
        if y_start_tune:
            y_start = np.min([y.min(), y_start])
        if y_end_tune:
            y_end = np.max([y.max(), y_end])

    if random != None:
        y = np.array([random]*x.size)
        if y_start_tune:
            y_start = np.min([y.min(), y_start])
        if y_end_tune:
            y_end = np.max([y.max(), y_end])
        plt.plot(x, y, linestyle="--", color="red", label="random")
    if approx_optimal != None:
        y = np.array([approx_optimal]*x.size)
        if y_start_tune:
            y_start = np.min([y.min(), y_start])
        if y_end_tune:
            y_end = np.max([y.max(), y_end]) * 1.1
        plt.plot(x, y, linestyle="--", color="green", label="approx_optimal")

    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.axis([x_start, x_end, y_start, y_end])
    # plt.subplots_adjust(right=.7)
    # plt.legend(bbox_to_anchor=(1.45, 1), loc=2)
    plt.legend(loc=2)
    plt.savefig(name, dpi=300)

files = glob.glob("./{}/*.log".format(plot_type))

Y = {}
for filename in files:
    with open(filename, "r") as log_file:
        data = log_file.read()

    words = filename.split("/")[-1].split(".")[0].split("_")[:-1]
    architecture = words[0]
    replay = " ".join(words[1:])
    # architecture, replay, _ = filename.split("/")[-1].split(".")[0].split("_")

    y = np.array(data.strip()[:-1].split(","), dtype=float)
    x = np.linspace(0, 5000, num=y.size)

    if architecture in Y:
        if replay not in Y[architecture]:
            Y[architecture][replay] = {}
            Y[architecture][replay]["data"] = y
            Y[architecture][replay]["count"] = 1
            Y[architecture][replay]["x"] = x
        else:
            Y[architecture][replay]["data"] += y
            Y[architecture][replay]["count"] += 1
    else:
        Y[architecture] = {}
        Y[architecture][replay] = {}
        Y[architecture][replay]["data"] = y
        Y[architecture][replay]["count"] = 1
        Y[architecture][replay]["x"] = x

for architecture in Y:
    for replay in Y[architecture]:
        Y[architecture][replay]["data"] = Y[architecture][replay]["data"] / Y[architecture][replay]["count"]
    # plot_save(Y[architecture]["x"], Y[architecture]["data"], architecture, name="./{}/plots/{}".format(plot_type, architecture))

# with open("{}/random.txt".format(plot_type)) as _file:
#     random = float(_file.read().strip())
#
# with open("{}/approx_optimal.txt".format(plot_type)) as _file:
#     approx_optimal = float(_file.read().strip())

# plot_save_multi(Y, "Validation Scores for Multiple Architectures", random, approx_optimal, name="./{}/plots/multi".format(plot_type))
for architecture in Y:
    plot_save_multi(Y[architecture], "Validation Scores for Training Methods {}".format(architecture), name="./{}/plots/{}".format(plot_type, architecture))

# plot_save(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, smooth_y, "smoother")
