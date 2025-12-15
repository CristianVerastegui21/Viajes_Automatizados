import pandas as pd
from scipy.stats import shapiro

# --- INGRESA AQUÍ tus 30 valores del pretest y postest ---
pretest = [
7.75,6.38,8.06,9.57,6.12,6.12,9.77,8.43,6.51,7.54,
5.53,8.08,6.47,7.88,6.84,8.52,7.82,7.35,6.17,8.77,
6.70,5.74,7.13,7.98,6.41,7.29,8.60,6.32,7.94,7.55
]

postest = [
2.35,1.92,2.28,1.30,2.40,2.22,1.83,2.07,3.06,1.79,
2.86,0.97,1.88,1.95,1.99,2.71,1.61,2.49,2.02,1.88,
0.95,2.29,2.76,1.82,2.69,2.25,2.41,1.87,1.52,2.33
]

# --- Shapiro-Wilk ---
w_pre, p_pre = shapiro(pretest)
w_post, p_post = shapiro(postest)

print("RESULTADOS PRETEST:")
print("W =", w_pre)
print("p =", p_pre)

print("\nRESULTADOS POSTEST:")
print("W =", w_post)
print("p =", p_post)
