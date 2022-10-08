from matplotlib import pyplot as plt
import numpy as np


def step(xs, yss):
    return xs * yss * (1 - yss)


def grid(y_min=0.1, y_max=0.9, y_count=100, x_min=0, x_max=4, x_count=10000):
    xs = np.linspace(x_min, x_max, x_count)[:, None]
    ys = np.linspace(y_min, y_max, y_count)[None, :]
    yss = np.tile(ys, (x_count, 1))
    return xs, yss


def N_steps(N, xs, yss):
    for _ in range(N):
        yss = step(xs, yss)
    return xs, yss


def plot_grid(xs, yss):
    fig = plt.figure()
    for x, ys in zip(xs, yss):
        plt.scatter(
            np.repeat(x, len(ys)),
            ys,
            marker=",",
            s=(72.0 / fig.dpi) ** 2,
            lw=0,
            c="blue",
        )
    plt.show()


plot_grid(*N_steps(100, *grid()))
