import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

print("Dibujando el grafo del Sudoku...")
nodos_df = pd.read_csv("dataset/sudoku_nodes.csv")
aristas_df = pd.read_csv("dataset/sudoku_edges.csv")

G = nx.Graph()

sub_nodos = nodos_df[nodos_df['tablero'] == 0]
sub_aristas = aristas_df[(aristas_df['origen'] < 81) & (aristas_df['destino'] < 81)]

G.add_nodes_from(sub_nodos['node_id'])
G.add_edges_from(zip(sub_aristas['origen'], sub_aristas['destino']))

plt.figure(figsize=(8,8))

pos = {row['node_id']: (row['columna'], -row['fila']) for _, row in sub_nodos.iterrows()}
nx.draw(G, pos, node_size=400, node_color='#4F81BD', edge_color='#cccccc', with_labels=True, font_size=8, font_color='white')

os.makedirs("report/assets", exist_ok=True)
plt.savefig("report/assets/sudoku_graph.png")
print("✅ ¡Imagen guardada en report/assets/sudoku_graph.png!")