import pandas as pd
from scipy.stats import shapiro, wilcoxon, ttest_rel
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_excel("tiempos_pre_post.xlsx")

pre = df["pretest"]
post = df["postest"]

print("\nDATOS CARGADOS:")
print(df.head())

# ----------------------------------------------------------
# 1. GRÁFICOS DESCRIPTIVOS
# ----------------------------------------------------------

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
sns.boxplot(data=[pre, post])
plt.xticks([0,1], ["Pretest", "Postest"])
plt.title("Boxplot de tiempos")

plt.subplot(1,2,2)
sns.histplot(pre, color="blue", kde=True, label="Pretest")
sns.histplot(post, color="red", kde=True, label="Postest")
plt.legend()
plt.title("Distribución Pretest vs Postest")

plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# 2. Normalidad: Shapiro-Wilk
# ----------------------------------------------------------

print("\n--- PRUEBA SHAPIRO–WILK ---")
sh_pre = shapiro(pre)
sh_post = shapiro(post)

print("Pretest:", sh_pre)
print("Postest:", sh_post)

# ----------------------------------------------------------
# 3. Pruebas inferenciales
# ----------------------------------------------------------

print("\n--- PRUEBA DE WILCOXON ---")
wilcox = wilcoxon(pre, post)
print(wilcox)

print("\n--- PRUEBA T PAREADA (SOLO COMO COMPLEMENTO) ---")
t_test = ttest_rel(pre, post)
print(t_test)
