import pandas as pd
import os
import time

def generar_grafo_sudoku_generalizado(k=7):
    """
    Genera el grafo de restricciones para un Sudoku generalizado de orden k.
    Dimensiones del tablero: N x N donde N = k^2.
    Total de nodos (variables/celdas): N^2 = k^4.
    Para k=7: N=49, total nodos = 2,401.
    Grado de cada nodo: 3N - 2k - 1 = 132.
    Total aristas: (2,401 * 132) / 2 = 158,466.
    """
    t0 = time.time()
    N = k * k
    total_nodes = N * N
    print("=== Generando Grafo de Restricciones: Sudoku Generalizado N x N ===")
    print(f"Parametro de orden k: {k}")
    print(f"Dimensiones de la cuadricula (N x N): {N} x {N}")
    print(f"Subbloques: {k} x {k}")
    print(f"Total de celdas (Vertices): {total_nodes}")

    nodos = []
    from collections import defaultdict
    row_groups = defaultdict(list)
    col_groups = defaultdict(list)
    box_groups = defaultdict(list)

    for r in range(N):
        for c in range(N):
            node_id = r * N + c
            bloque_id = (r // k) * k + (c // k)
            nodos.append({
                'node_id': node_id,
                'fila': r,
                'columna': c,
                'bloque': bloque_id,
                'orden_k': k
            })
            row_groups[r].append(node_id)
            col_groups[c].append(node_id)
            box_groups[bloque_id].append(node_id)

    edge_set = set()
    for grp in [row_groups, col_groups, box_groups]:
        for members in grp.values():
            L = len(members)
            for i in range(L):
                u = members[i]
                for j in range(i + 1, L):
                    v = members[j]
                    if u < v:
                        edge_set.add((u, v))
                    else:
                        edge_set.add((v, u))

    aristas = [{'origen': u, 'destino': v, 'tipo': 'restriccion_diferente'} for u, v in sorted(edge_set)]

    os.makedirs("dataset", exist_ok=True)
    pd.DataFrame(nodos).to_csv("dataset/sudoku_nodes.csv", index=False)
    pd.DataFrame(aristas).to_csv("dataset/sudoku_edges.csv", index=False)
    
    t1 = time.time()
    print(f"Exito: Generados {len(nodos)} nodos y {len(aristas)} aristas en {t1 - t0:.2f} segundos.")
    print("Archivos exportados en 'dataset/sudoku_nodes.csv' y 'dataset/sudoku_edges.csv'.")

if __name__ == "__main__":
    generar_grafo_sudoku_generalizado(k=7)
