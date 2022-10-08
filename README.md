# Logistic map computation

This a simple computation of logistic map fractal.
1 milion of points is produced randomly, and each is then evolved for 500 generations.
Results are stored as files after each 10 generations (for the first 10 generation after each generation).

To produce final gif, run from terminal:

```
pip install -r requirements.txt
python logistic_map_compute.py
python plot_results.py
```