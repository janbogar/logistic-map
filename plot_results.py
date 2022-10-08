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
        for n,i in enumerate(iter):
            print(f"Processing value {i} (processed so far: {n})")
            yield i
            
os.makedirs("figs",exist_ok=True)

MAX_GENERATION=300

files_per_generation=defaultdict(list)

name_re = re.compile(r"(?P<name>.*)_worker=(?P<worker>\d+)_generations=(?P<generations>\d+).txt")
for path in Path("data").iterdir():
    match=name_re.match(str(path)) 
    if match:
        files_per_generation[int(match.group("generations"))].append(path)

print(f"Found {sum(map(len,files_per_generation.values()))} files with results from {len(files_per_generation)} different generations.")

def read_file(path):
    f=open(path)

    header={}
    for line in f:
        if re.match("-+",line.strip()):   
           break
        else:
            key,value=line.split(":")
            header[key.strip()]=int(value.strip())
    
    return header,np.array([[float(i) for i in split_line] for split_line in (line.strip().split(", ") for line in f)])

def plot_data(x,y, generation, path):
    dpi=500
    fig=plt.figure(dpi=dpi)
    plt.scatter(x,y,marker=",",s=(72./fig.dpi)**2,lw=0,c="navy")
    plt.suptitle(f"Počet generácií králikov= {generation}")
    plt.xlabel("Počet potomkov na králika")
    plt.ylabel("Populácia (ako zlomok z maximálnej kapacity prostredia)")

    plt.tight_layout()
    plt.savefig(path,dpi=dpi)

def load_data(files_per_generation,generation):
    headers,data=zip(*map(read_file,files_per_generation[generation]))
    headers=list(headers)
    data=np.vstack(data)
    assert(sorted([i["worker"] for i in headers])==list(range(len(headers))))
    assert (data.shape == (sum([i["N_points"] for i in headers]),3))
    assert(all((i["generations"]==generation for i in headers)))
    return headers,data

def get_fig_path(generation):
    return Path(f"figs/fig_{generation}.png")

figures=[]

print("Plotting generations")
generation=0
path=get_fig_path(generation)
if not path.exists():
    _,data=load_data(files_per_generation,min(files_per_generation.keys()))
    plot_data(data[:,0],data[:,1],generation,str(path))   # drawing different column
figures.append(path)

to_plot = [i for i in sorted(files_per_generation.keys()) if i<=MAX_GENERATION]

for generation in tqdm(to_plot):
    path=get_fig_path(generation)
    if not path.exists():
        _,data=load_data(files_per_generation,generation)
        plot_data(data[:,0],data[:,2],generation,path)
    figures.append(path)

for i in range(10):
    figures.append(path)

print("Producing gif.")
with imageio.get_writer('logisticka_mapa.gif', mode='I',fps=7) as writer:
    for filename in tqdm(figures):
        image = imageio.imread(filename)
        writer.append_data(image)

        

    