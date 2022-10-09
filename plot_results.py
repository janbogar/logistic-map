import matplotlib.pyplot as plt
from pathlib import Path
import regex as re
from collections import defaultdict
import numpy as np
import os
import imageio

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iter):
        for n, i in enumerate(iter):
            print(f"Processing value {i} (processed so far: {n})")
            yield i


os.makedirs("figs", exist_ok=True)

MAX_GENERATION = 300
LANGUAGE = "en"
DPI = 500
WORKERS_TO_PLOT = "all"

plot_texts = {
    "sk": {
        "title": "Počet generácií králikov= {}",
        "xlabel": "Počet potomkov na králika",
        "ylabel": "Populácia (ako zlomok z maximálnej kapacity prostredia)",
    },
    "en": {
        "title": "Generation= {}",
        "xlabel": "Number of children per individual",
        "ylabel": "Population (as fraction of maximal capacity of environment)",
    },
}

files_per_generation = defaultdict(list)

name_re = re.compile(
    r"(?P<name>.*)_worker=(?P<worker>\d+)_generations=(?P<generations>\d+).txt"
)
for path in Path("data").iterdir():
    match = name_re.match(str(path))
    if match:
        if WORKERS_TO_PLOT != "all":
            if int(match.group("worker")) in WORKERS_TO_PLOT:
                files_per_generation[int(match.group("generations"))].append(path)

print(
    f"Found {sum(map(len,files_per_generation.values()))} files with results for {len(files_per_generation)} different generations."
)


def read_file(path):
    f = open(path)

    header = {}
    for line in f:
        if re.match("-+", line.strip()):
            break
        else:
            key, value = line.split(":")
            header[key.strip()] = int(value.strip())

    return header, np.array(
        [
            [float(i) for i in split_line]
            for split_line in (line.strip().split(", ") for line in f)
        ]
    )


def plot_data(x, y, generation, path, language=LANGUAGE, dpi=DPI):
    fig = plt.figure(dpi=dpi)
    plt.scatter(x, y, marker=",", s=(72.0 / fig.dpi) ** 2, lw=0, c="navy")
    plt.title(plot_texts[language]["title"].format(generation))
    plt.xlabel(plot_texts[language]["xlabel"])
    plt.ylabel(plot_texts[language]["ylabel"])

    plt.tight_layout()
    plt.savefig(path, dpi=dpi)
    plt.close("all")


def load_data(files_per_generation, generation):
    headers, data = zip(*map(read_file, files_per_generation[generation]))
    headers = list(headers)
    data = np.vstack(data)

    assert sorted([i["worker"] for i in headers]) == list(range(len(headers)))
    assert data.shape == (sum([i["N_points"] for i in headers]), 3)
    assert all((i["generations"] == generation for i in headers))
    return headers, data


def get_fig_path(generation):
    return Path(f"figs/fig_{generation}.png")


figures = []
to_plot = [i for i in sorted(files_per_generation.keys()) if i <= MAX_GENERATION]

print(f"Plotting generations (total number of plots: {len(to_plot)})")
generation = 0
path = get_fig_path(generation)
if not path.exists():
    _, data = load_data(files_per_generation, min(files_per_generation.keys()))
    plot_data(
        data[:, 0], data[:, 1], generation, str(path), language=LANGUAGE
    )  # drawing different column
figures.append(path)


for generation in tqdm(to_plot):
    path = get_fig_path(generation)
    if not path.exists():
        _, data = load_data(files_per_generation, generation)
        plot_data(data[:, 0], data[:, 2], generation, path, language=LANGUAGE)
    figures.append(path)

# last figure lasts longer
for i in range(10):
    figures.append(path)

print("Producing gif")
with imageio.get_writer("logistic_map.gif", mode="I", fps=7) as writer:
    for filename in tqdm(figures):
        image = imageio.imread(filename)
        writer.append_data(image)
