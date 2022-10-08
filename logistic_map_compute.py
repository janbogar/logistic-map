from multiprocessing import Process
from random import Random
import numpy as np
import os

os.makedirs("data", exist_ok=True)

y_min = 0.1
y_max = 0.9
x_min = 0
x_max = 4

workers = 8
generation_steps = [1 for i in range(10)] + [10 for i in range(48)]
N_points = 1000000  # how many points should each worker calculate


def evolve(x, y, generations):
    for _ in range(generations):
        y = x * y * (1 - y)
    return y


def random_points(N_points, y_min, y_max, x_min, x_max, seed):
    rng = np.random.default_rng(seed=42)
    xs = rng.random((N_points,)) * (x_max - x_min) + x_min
    ys = rng.random((N_points,)) * (y_max - y_min) + y_min
    return xs, ys


def header(worker, N_points, generations, seed, file):
    print("worker: ", worker, file=file)
    print("N_points: ", N_points, file=file)
    print("generations: ", generations, file=file)
    print("seed: ", seed, file=file)
    print("-------------------", file=file)


def do_the_thing(
    worker, filename_base, generation_steps, N_points, y_min, y_max, x_min, x_max, seed
):

    xs, ys = random_points(N_points, y_min, y_max, x_min, x_max, seed)

    total_generations = 0
    for generation_step in generation_steps:
        new_ys = evolve(xs, ys, generation_step)
        total_generations += generation_step
        with open(
            f"{filename_base}_worker={worker}_generations={total_generations}.txt", "w"
        ) as f:
            header(worker, N_points, total_generations, seed, f)
            for x, y, new_y in zip(xs, ys, new_ys):
                print(", ".join([str(i) for i in [x, y, new_y]]), file=f)
        ys = new_ys
    return ys


processes = []

for i in range(workers):
    processes.append(
        Process(
            target=do_the_thing,
            args=(
                i,
                "data/logistic_map",
                generation_steps,
                N_points,
                y_min,
                y_max,
                x_min,
                x_max,
                i * 42,
            ),
        )
    )

for p in processes:
    p.start()

for p in processes:
    p.join()

print("done")
