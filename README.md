# Logistic map fractal
This is a simple computation of attractor of logistic map.
1 milion of points is produced randomly, and each is then evolved for 500 generations.
Results are stored as files after each 10 generations (for the first 10 generation after each generation).

To produce final gif, run these commands from terminal:

```
pip install -r requirements.txt
python logistic_map_compute.py
python plot_results.py
```