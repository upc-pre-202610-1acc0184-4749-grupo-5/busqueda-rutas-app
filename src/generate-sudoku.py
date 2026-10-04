import pandas as pd
import os

print("Generando red de restricciones para 20 tableros de Sudoku...")
NUM_TABLEROS = 20
nodos = []
aristas = []

for b in range(NUM_TABLEROS):
    for r in range(9):
        for c in range(9):
            nodo_id = b * 81 + r * 9 + c
            nodos.append({'node_id': nodo_id, 'tablero': b, 'fila': r, 'columna': c})
            
    for i in range(81):
        for j in range(i + 1, 81):
            r1, c1 = i // 9, i % 9
            r2, c2 = j // 9, j % 9
            if r1 == r2 or c1 == c2 or (r1//3 == r2//3 and c1//3 == c2//3):
                aristas.append({'origen': b * 81 + i, 'destino': b * 81 + j, 'tipo': 'restriccion'})

os.makedirs("dataset", exist_ok=True)
pd.DataFrame(nodos).to_csv("dataset/sudoku_nodes.csv", index=False)
pd.DataFrame(aristas).to_csv("dataset/sudoku_edges.csv", index=False)
print(f"✅ ¡Éxito! Generados {len(nodos)} nodos y {len(aristas)} aristas en la carpeta 'dataset/'.")