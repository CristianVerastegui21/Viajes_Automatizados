import numpy as np
import pandas as pd

# reproducibilidad
np.random.seed(42)

# generar 30 valores simulados para pretest y postest
pretest = np.random.normal(loc=7.0, scale=1.5, size=30)
postest = np.random.normal(loc=2.0, scale=0.7, size=30)

# crear dataframe
df = pd.DataFrame({
    "pretest": pretest,
    "postest": postest
})

# guardar a Excel
df.to_excel("tiempos_pre_post.xlsx", index=False)

print("Archivo generado: tiempos_pre_post.xlsx")
