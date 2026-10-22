import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

print("=== Generando Visualización del Grafo de Sudoku con Partición por Integrante ===")
nodos_df = pd.read_csv("dataset/sudoku_nodes.csv")
aristas_df = pd.read_csv("dataset/sudoku_edges.csv")

os.makedirs("report/assets", exist_ok=True)

# Mapeo de colores y etiquetas de integrantes
# Kobashigawa 800 nodos, Pareja 801 nodos, Riveros 800 nodos
COLOR_MAP = {
    "Kobashigawa Ugaz, Juan Alejandro": "#1F77B4",  # Azul clásico
    "Pareja Calloapaza, Marcelo Fausto": "#2CA02C", # Verde esmeralda
    "Riveros Mera, Jennifer Yamilet": "#D62728"    # Rojo carmesí
}

SHORT_NAMES = {
    "Kobashigawa Ugaz, Juan Alejandro": "Kobashigawa Ugaz, J.: 800 nodos",
    "Pareja Calloapaza, Marcelo Fausto": "Pareja Calloapaza, M.: 801 nodos",
    "Riveros Mera, Jennifer Yamilet": "Riveros Mera, J.: 800 nodos"
}

nodos_df['color'] = nodos_df['integrante'].map(COLOR_MAP)

# Configuracion de figura de alta resolucion con mayor espacio vertical para evitar cualquier solapamiento
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17, 8.5), dpi=300)

# -------------------------------------------------------------
# PANEL 1: Grafo Completo (Grid N=49x49 = 2,401 nodos particionados)
# -------------------------------------------------------------
pos_full = {row['node_id']: (row['columna'], -row['fila']) for _, row in nodos_df.iterrows()}

# Dibujar una muestra representativa de aristas de restriccion de fondo
sample_edges = aristas_df[aristas_df['origen'] % 35 == 0]
sample_edge_tuples = list(zip(sample_edges['origen'], sample_edges['destino']))

G_full = nx.Graph()
G_full.add_nodes_from(nodos_df['node_id'])
G_full.add_edges_from(sample_edge_tuples)

nx.draw_networkx_edges(G_full, pos_full, ax=ax1, alpha=0.08, edge_color='#444444', width=0.5)

# Dibujar nodos agrupados por integrante
for integrante, color in COLOR_MAP.items():
    sub_df = nodos_df[nodos_df['integrante'] == integrante]
    ax1.scatter(sub_df['columna'], -sub_df['fila'], c=color, s=14, label=SHORT_NAMES[integrante], alpha=0.9, edgecolors='none')

# Lineas divisorias de bloques 7x7 para orientacion espacial de la cuadricula
for i in range(0, 50, 7):
    ax1.axvline(i - 0.5, color='#B0BEC5', linestyle='--', linewidth=0.6, alpha=0.55)
    ax1.axhline(-i + 0.5, color='#B0BEC5', linestyle='--', linewidth=0.6, alpha=0.55)

# Badges informativos de particion ubicados estrategicamente
ax1.text(24, -7.5, "Partición Kobashigawa: 800 nodos (Filas 0-16)", fontsize=8, color="#0D47A1", fontweight='bold', ha='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#E3F2FD", ec="#1F77B4", lw=1.2, alpha=0.92))
ax1.text(24, -24.5, "Partición Pareja: 801 nodos (Filas 16-32)", fontsize=8, color="#1B5E20", fontweight='bold', ha='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#E8F5E9", ec="#2CA02C", lw=1.2, alpha=0.92))
ax1.text(24, -41.5, "Partición Riveros: 800 nodos (Filas 32-48)", fontsize=8, color="#B71C1C", fontweight='bold', ha='center',
         bbox=dict(boxstyle="round,pad=0.3", fc="#FFEBEE", ec="#D62728", lw=1.2, alpha=0.92))

ax1.set_title("A. Grafo Completo de Restricciones (N=49, |V|=2,401 celdas)\nDistribución de Nodos por Integrante (Rúbrica >= 500 nodos c/u)", 
              fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("Coordenada Columna (0 a 48)", fontsize=9, labelpad=5)
ax1.set_ylabel("Coordenada Fila (0 a -48)", fontsize=9, labelpad=5)
ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=True, fontsize=7.8)
ax1.set_xlim(-2, 50)
ax1.set_ylim(-50, 2)
ax1.set_aspect('equal')

# -------------------------------------------------------------
# PANEL 2: Subgrafo Representativo de Intersección Multi-Integrante
# -------------------------------------------------------------
# Seleccionar celdas representativas que cruzan las 3 particiones y comparten aristas de restriccion mutua
sub_koba = nodos_df[(nodos_df['integrante'] == "Kobashigawa Ugaz, Juan Alejandro") & (nodos_df['columna'].between(22, 26)) & (nodos_df['fila'].between(12, 15))]
sub_pareja = nodos_df[(nodos_df['integrante'] == "Pareja Calloapaza, Marcelo Fausto") & (nodos_df['columna'].between(22, 26)) & (nodos_df['fila'].between(17, 20))]
sub_riveros = nodos_df[(nodos_df['integrante'] == "Riveros Mera, Jennifer Yamilet") & (nodos_df['columna'].between(22, 26)) & (nodos_df['fila'].between(33, 36))]

sub_focal_df = pd.concat([sub_koba, sub_pareja, sub_riveros]).drop_duplicates(subset=['node_id'])
sub_focal_ids = set(sub_focal_df['node_id'])

# Extraer aristas inducidas entre estos nodos
sub_focal_edges = aristas_df[aristas_df['origen'].isin(sub_focal_ids) & aristas_df['destino'].isin(sub_focal_ids)]

G_sub = nx.Graph()
for _, row in sub_focal_df.iterrows():
    G_sub.add_node(row['node_id'], color=COLOR_MAP[row['integrante']], integrante=row['integrante'])

for _, row in sub_focal_edges.iterrows():
    G_sub.add_edge(row['origen'], row['destino'])

pos_sub = nx.spring_layout(G_sub, seed=42, k=0.45)

node_colors_sub = [G_sub.nodes[n]['color'] for n in G_sub.nodes()]

# Dibujar aristas con estilo
nx.draw_networkx_edges(G_sub, pos_sub, ax=ax2, alpha=0.35, edge_color='#78909C', width=1.2)
nx.draw_networkx_nodes(G_sub, pos_sub, ax=ax2, node_color=node_colors_sub, node_size=290, edgecolors='#263238', linewidths=1.0)
nx.draw_networkx_labels(G_sub, pos_sub, ax=ax2, font_size=6.2, font_color='white', font_family='sans-serif', font_weight='bold')

# Leyenda explicativa en Panel 2
legend_elements = [
    mpatches.Patch(facecolor='#1F77B4', edgecolor='#0D47A1', label='Kobashigawa: 800 nodos (Filas 0-16)'),
    mpatches.Patch(facecolor='#2CA02C', edgecolor='#1B5E20', label='Pareja: 801 nodos (Filas 16-32)'),
    mpatches.Patch(facecolor='#D62728', edgecolor='#B71C1C', label='Riveros: 800 nodos (Filas 32-48)'),
    mpatches.Patch(facecolor='#78909C', edgecolor='none', label='Aristas: Restricciones mutuas (u != v)')
]
ax2.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=True, fontsize=7.8)

ax2.set_title("B. Subgrafo Inducido de Restricciones Mutuas entre Integrantes\nInterconexión de Nodos y Restricciones Compartidas (Aristas u != v)", 
              fontsize=11, fontweight='bold', pad=10)
ax2.axis('off')

# Titulo superior general con ajuste de coordenadas para evitar solapamientos
fig.suptitle("Grafo de Restricciones del Sudoku Generalizado N=49 (k=7) — Total 2,401 Nodos\nDivisión Equitativa del Modelado por Integrante según Rúbrica UPC (Kobashigawa: 800, Pareja: 801, Riveros: 800)", 
             fontsize=12.5, fontweight='bold', y=0.97)

plt.subplots_adjust(top=0.86, bottom=0.15, left=0.06, right=0.96, wspace=0.18)
output_path = "report/assets/sudoku_graph.png"
plt.savefig(output_path, dpi=300)
plt.close()

print(f"Exito: Imagen guardada en '{output_path}'.")
