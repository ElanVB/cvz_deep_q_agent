import numpy as np, glob, os
from matplotlib import pyplot as plt

plot_type = "validation"
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

def plot_save_multi(Y, title, x_axis='Episode', y_axis='Score',
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

    plt.figure()

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

    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.axis([x_start, x_end, y_start, y_end])
    plt.legend()
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

plot_save_multi(Y, "Variation Scores for Multiple Architectures", name="./{}/plots/multi".format(plot_type))

# plot_save(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, y, "Validation Score versus Episodes for Network 1")
# plot_show(x, smooth_y, "smoother")
