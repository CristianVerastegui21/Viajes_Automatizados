import pandas as pd
import pingouin as pg

# -----------------------------
# Cargar archivo
# -----------------------------
df = pd.read_excel("encuesta.xlsx")

# Eliminar columna no numérica
df = df.drop(columns=["Encuestado"])

print("DATOS CARGADOS:")
print(df.head())

# -----------------------------
# Alfa de Cronbach con pingouin
# -----------------------------
alpha = pg.cronbach_alpha(data=df)
print("\nAlfa de Cronbach:", alpha)

# -----------------------------
# Omega de McDonald (compatible)
# -----------------------------
from factor_analyzer.factor_analyzer import FactorAnalyzer

def calculate_omega(df):
    fa = FactorAnalyzer(rotation=None, n_factors=1)
    fa.fit(df)

    loadings = fa.loadings_
    loadings = loadings.flatten()

    # Varianzas
    common_variance = sum(loadings**2)
    unique_variance = df.shape[1] - common_variance

    omega = common_variance / (common_variance + unique_variance)
    return omega

omega_value = calculate_omega(df)
print("\nOmega de McDonald:", omega_value)
