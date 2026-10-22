import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

print("Visualizando el grafo de restricciones del Sudoku...")
nodos_df = pd.read_csv("dataset/sudoku_nodes.csv")
aristas_df = pd.read_csv("dataset/sudoku_edges.csv")

os.makedirs("report/assets", exist_ok=True)

# 1. Visualizacion del Subgrafo representativo: Bloque y celda focal
# Para que la imagen sea legible y represente fielmente la estructura de cliques y restricciones de fila/columna/bloque
# Tomamos el bloque 0 (celdas de la region 0 <= fila < 7, 0 <= col < 7 -> 49 celdas formando un clique perfecto)
# y anadimos las conexiones cruzadas de fila 0 y col 0 completas.
sub_nodos = nodos_df[nodos_df['bloque'] == 0]
sub_node_ids = set(sub_nodos['node_id'])

# Aristas internas del subgrafo (clique del bloque)
sub_edges = aristas_df[aristas_df['origen'].isin(sub_node_ids) & aristas_df['destino'].isin(sub_node_ids)]

G_sub = nx.Graph()
G_sub.add_nodes_from(sub_nodos['node_id'])
G_sub.add_edges_from(zip(sub_edges['origen'], sub_edges['destino']))

fig, ax = plt.subplots(figsize=(9, 9), dpi=300)

pos = {row['node_id']: (row['columna'], -row['fila']) for _, row in sub_nodos.iterrows()}

nx.draw_networkx_edges(G_sub, pos, ax=ax, alpha=0.35, edge_color='#888888', width=1.0)
nx.draw_networkx_nodes(G_sub, pos, ax=ax, node_size=320, node_color='#2F5496', edgecolors='#1B365D', linewidths=1.2)
nx.draw_networkx_labels(G_sub, pos, ax=ax, font_size=7, font_color='white', font_family='sans-serif', font_weight='bold')

ax.set_title("Subgrafo de Restricciones del Sudoku Generalizado N=49 (k=7)\nClique de 49 celdas en el Subbloque 0 (Restricciones Mutuas)", fontsize=12, fontweight='bold', pad=15)
ax.axis('off')

plt.tight_layout()
plt.savefig("report/assets/sudoku_graph.png", dpi=300)
plt.close()
print("Grafico guardado exitosamente en 'report/assets/sudoku_graph.png'.")
