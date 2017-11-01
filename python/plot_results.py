import numpy as np, glob, os
from matplotlib import pyplot as plt

plot_type = "validation_simple_reward"
# plot_type = "network_update_long"
# plot_type = "validate_large_net"
# plot_type = "validate_150"
# plot_type = "validation_long_term"
# plot_type = "replay_sample"
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

    for architecture in Y:
        y = Y[architecture]["data"]
        x = Y[architecture]["x"]
        plt.plot(x, y, label=architecture)

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

# def plot_show(x, y, title, x_axis='Episode', y_axis='Score', x_start=None, x_end=None, y_start=None, y_end=None):
#     if x_start == None:
#         x_start = x.min()
#     if x_end == None:
#         x_end = x.max()
#     if y_start == None:
#         y_start = y.min()
#     if y_end == None:
#         y_end = y.max()
#
#     plt.figure()
#
#     plt.plot(x, y, color="blue")
#     plt.title(title)
#     plt.xlabel(x_axis)
#     plt.ylabel(y_axis)
#     plt.axis([x_start, x_end, y_start, y_end])
#     plt.show()

files = glob.glob("./{}/*.log".format(plot_type))

Y = {}
for filename in files:
    with open(filename, "r") as log_file:
        data = log_file.read()

    architecture, _ = filename.split("/")[-1].split(".")[0].split("_")

    y = np.array(data[:-1].split(","), dtype=float)

    # for _ in range(15):
    #     y = np.concatenate([[y[0]], (y[:-1] + y[1:])/2, [y[-1]]])

    x = np.linspace(0, 5000, num=y.size)

    if architecture in Y:
        Y[architecture]["data"] += y
        Y[architecture]["count"] += 1
    else:
        Y[architecture] = {}
        Y[architecture]["data"] = y
        Y[architecture]["count"] = 1
        Y[architecture]["x"] = x

for architecture in Y:
    Y[architecture]["data"] = Y[architecture]["data"] / Y[architecture]["count"]
    plot_save(Y[architecture]["x"], Y[architecture]["data"], architecture, name="./{}/plots/{}".format(plot_type, architecture))

with open("{}/random.txt".format(plot_type)) as _file:
    random = float(_file.read().strip())

with open("{}/approx_optimal.txt".format(plot_type)) as _file:
    approx_optimal = float(_file.read().strip())

plot_save_multi(Y, "Validation Score for the Simple Reward System", random, approx_optimal, name="./{}/plots/multi".format(plot_type))

# plot_save(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, smooth_y, "smoother")
