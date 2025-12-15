import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# ---------------------------------------
# CONFIGURACIÓN DE VALORES (CAMBIAR AQUÍ)
# ---------------------------------------

# Omega Pretest y Postest (reales o calculados)
omega_pretest = 0.58
omega_postest = 0.63

# Cargas factoriales simuladas (estas se reemplazan con las reales si las tienes)
loadings_pretest = [0.55, 0.50, 0.48, 0.60, 0.52]   # Pretest
loadings_postest = [0.63, 0.61, 0.58, 0.65, 0.60]   # Postest

items = ["Item1", "Item2", "Item3", "Item4", "Item5"]

# ------------------------------------------------------
# FUNCIÓN PARA GENERAR EL DIAGRAMA FACTORIAL TIPO SEM
# ------------------------------------------------------

def dibujar_omega(loadings, omega, titulo):

    G = nx.DiGraph()

    # Nodo del factor general
    G.add_node("g")

    # Crear nodos de ítems y flechas del factor g → ítem
    for item, carga in zip(items, loadings):
        G.add_node(item)
        G.add_edge("g", item, weight=round(carga, 2))

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(9, 6))
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightblue")
    
    # Dibujar etiquetas
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    # Dibujar flechas con cargas factoriales
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

    # Dibujar etiquetas de cargas factoriales
    edge_labels = {(u, v): d["weight"] for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title(f"{titulo}\nOmega = {omega}", fontsize=14)
    plt.axis("off")
    plt.show()

# ------------------------------
# GRAFICO PRETEST
# ------------------------------
dibujar_omega(loadings_pretest, omega_pretest, "Modelo factorial - PRETEST")

# ------------------------------
# GRAFICO POSTEST
# ------------------------------
dibujar_omega(loadings_postest, omega_postest, "Modelo factorial - POSTEST")
