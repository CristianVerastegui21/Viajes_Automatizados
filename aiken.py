import numpy as np
import pandas as pd

# EJEMPLO: valores dados por 3 jueces para 1 ítem (calidad global)
ratings = np.array([5, 5, 4])   # r_j
n = len(ratings)
c = 5   # escala 1-5
l = 1

# Cálculo directo de V
s = ratings - l
S = s.sum()
V = S / (n * (c - 1))
print("V de Aiken:", V)

# Bootstrap para IC (por ejemplo 95%)
def bootstrap_V(ratings, n_boot=10000, random_state=42):
    rng = np.random.default_rng(random_state)
    boot_vs = []
    for _ in range(n_boot):
        sample = rng.choice(ratings, size=len(ratings), replace=True)
        s = sample - l
        Vb = s.sum() / (len(sample) * (c - 1))
        boot_vs.append(Vb)
    return np.percentile(boot_vs, [2.5, 97.5]), np.mean(boot_vs)

ci, v_mean = bootstrap_V(ratings)
print("Bootstrap mean V:", v_mean)
print("IC 95% bootstrap para V:", ci)
