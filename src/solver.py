"""
solver.py
=========
Módulo de Algoritmia y Complejidad para la resolución de Sudokus Generalizados N x N.
Desarrollado para el Hito 2 (TB2) - Complejidad Algorítmica (CC184).
Autor: Pareja Calloapaza, Marcelo Fausto (u202411627)

Implementa y compara dos estrategias algorítmicas de búsqueda sobre el grafo de restricciones:
1. Backtracking Clásico con Búsqueda en Profundidad (DFS Secuencial).
2. Backtracking Optimizado con Heurística MRV (Minimum Remaining Values)
   con Bitmasks y Poda Sistemática (Forward Checking).
"""

import time
from typing import List, Tuple, Optional, Dict


class SudokuSolver:
    def __init__(self, board: List[List[int]], k: int = 3):
        """
        Inicializa el resolutor para un tablero generalizado de orden k.
        Dimensiones: N x N donde N = k^2.
        Valores válidos: 1 a N (0 representa celda vacía).
        """
        self.k = k
        self.N = k * k
        self.board = [row[:] for row in board]
        
        # Métricas de rendimiento algorítmico
        self.backtracks = 0
        self.nodes_explored = 0
        self.execution_time = 0.0

    # =========================================================================
    # ESTRATEGIA 1: BACKTRACKING BÁSICO (DFS SECUENCIAL)
    # =========================================================================
    def is_valid_move(self, board: List[List[int]], row: int, col: int, val: int) -> bool:
        """Verificación estándar iterativa en tiempo O(N)."""
        for c in range(self.N):
            if board[row][c] == val:
                return False
        for r in range(self.N):
            if board[r][col] == val:
                return False
        start_r = (row // self.k) * self.k
        start_c = (col // self.k) * self.k
        for r in range(start_r, start_r + self.k):
            for c in range(start_c, start_c + self.k):
                if board[r][c] == val:
                    return False
        return True

    def solve_basic(self) -> Tuple[bool, List[List[int]], Dict]:
        self.backtracks = 0
        self.nodes_explored = 0
        start_time = time.perf_counter()

        current_board = [row[:] for row in self.board]
        success = self._backtrack_basic(current_board)

        self.execution_time = (time.perf_counter() - start_time) * 1000

        metrics = {
            "algoritmo": "Backtracking Básico (DFS Secuencial)",
            "resuelto": success,
            "tiempo_ms": round(self.execution_time, 3),
            "nodos_explorados": self.nodes_explored,
            "backtracks": self.backtracks
        }
        return success, current_board, metrics

    def _find_empty_sequential(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        for r in range(self.N):
            for c in range(self.N):
                if board[r][c] == 0:
                    return r, c
        return None

    def _backtrack_basic(self, board: List[List[int]]) -> bool:
        empty = self._find_empty_sequential(board)
        if not empty:
            return True

        row, col = empty
        for val in range(1, self.N + 1):
            self.nodes_explored += 1
            if self.is_valid_move(board, row, col, val):
                board[row][col] = val
                if self._backtrack_basic(board):
                    return True
                board[row][col] = 0
                self.backtracks += 1

        return False

    # =========================================================================
    # ESTRATEGIA 2: BACKTRACKING CON HEURÍSTICA MRV OPTIMIZADA CON MÁSCARAS DE BITS
    # =========================================================================
    def solve_mrv(self) -> Tuple[bool, List[List[int]], Dict]:
        """
        Resuelve mediante Backtracking con MRV y Bitmasks O(1).
        Mantiene conjuntos de bits de valores usados por fila, columna y bloque,
        permitiendo calcular los candidatos legales mediante operaciones bitwise instantáneas.
        """
        self.backtracks = 0
        self.nodes_explored = 0
        start_time = time.perf_counter()

        current_board = [row[:] for row in self.board]

        # Máscaras de bits para números ya presentes: bit 'v' representa el valor 'v'
        row_masks = [0] * self.N
        col_masks = [0] * self.N
        box_masks = [0] * self.N
        empty_cells = []

        for r in range(self.N):
            for c in range(self.N):
                val = current_board[r][c]
                if val != 0:
                    bit = 1 << val
                    row_masks[r] |= bit
                    col_masks[c] |= bit
                    box_masks[(r // self.k) * self.k + (c // self.k)] |= bit
                else:
                    empty_cells.append((r, c))

        all_mask = (1 << (self.N + 1)) - 2  # Bits del 1 al N en 1

        success = self._backtrack_mrv_fast(current_board, empty_cells, row_masks, col_masks, box_masks, all_mask)

        self.execution_time = (time.perf_counter() - start_time) * 1000

        metrics = {
            "algoritmo": "Backtracking Optimizado con Heurística MRV + Bitmasks",
            "resuelto": success,
            "tiempo_ms": round(self.execution_time, 3),
            "nodos_explorados": self.nodes_explored,
            "backtracks": self.backtracks
        }
        return success, current_board, metrics

    def _backtrack_mrv_fast(self, board, empty_cells, row_masks, col_masks, box_masks, all_mask) -> bool:
        if not empty_cells:
            return True

        # Heurística MRV: Buscar la celda con menor cantidad de bits disponibles
        best_idx = -1
        best_candidates_mask = 0
        min_count = self.N + 2

        for i, (r, c) in enumerate(empty_cells):
            b_idx = (r // self.k) * self.k + (c // self.k)
            used = row_masks[r] | col_masks[c] | box_masks[b_idx]
            avail = all_mask & (~used)
            count = avail.bit_count()

            # Poda inmediata: si alguna celda no tiene opciones legales, este camino es un callejón sin salida
            if count == 0:
                self.backtracks += 1
                return False

            if count < min_count:
                min_count = count
                best_idx = i
                best_candidates_mask = avail
                if count == 1:
                    break  # Singleton: menor opción imposible, seleccionar de inmediato

        # Extraer la celda seleccionada por MRV
        r, c = empty_cells.pop(best_idx)
        b_idx = (r // self.k) * self.k + (c // self.k)

        # Probar cada candidato disponible
        mask = best_candidates_mask
        while mask > 0:
            # Obtener el bit menos significativo
            lowest_bit = mask & (-mask)
            val = lowest_bit.bit_length() - 1

            self.nodes_explored += 1
            board[r][c] = val
            row_masks[r] |= lowest_bit
            col_masks[c] |= lowest_bit
            box_masks[b_idx] |= lowest_bit

            if self._backtrack_mrv_fast(board, empty_cells, row_masks, col_masks, box_masks, all_mask):
                return True

            # Vuelta atrás (Backtrack)
            board[r][c] = 0
            row_masks[r] &= ~lowest_bit
            col_masks[c] &= ~lowest_bit
            box_masks[b_idx] &= ~lowest_bit
            self.backtracks += 1

            mask &= ~lowest_bit

        # Restaurar celda a la lista para niveles anteriores
        empty_cells.insert(best_idx, (r, c))
        return False


def print_board(board: List[List[int]], k: int = 3):
    N = k * k
    width = len(str(N)) + 1
    sep_line = "+" + "+".join(["-" * (k * width + 1)] * k) + "+"
    
    for r in range(N):
        if r % k == 0:
            print(sep_line)
        row_str = "| "
        for c in range(N):
            val_str = str(board[r][c]) if board[r][c] != 0 else "."
            row_str += val_str.rjust(width - 1) + " "
            if (c + 1) % k == 0:
                row_str += "| "
        print(row_str)
    print(sep_line)


if __name__ == "__main__":
    print("=" * 70)
    print("MÓDULO DE ALGORITMIA: BENCHMARKING DE RESOLUCIÓN DE SUDOKU")
    print("Autor: Pareja Calloapaza, Marcelo Fausto (u202411627)")
    print("=" * 70)

    # Instancia 9x9 difícil (17 pistas iniciales)
    board_9x9_hard = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]

    print("\n--- TABLERO ORIGINAL 9x9 (k=3) ---")
    print_board(board_9x9_hard, k=3)

    solver = SudokuSolver(board_9x9_hard, k=3)

    print("\n1. Ejecutando Backtracking Básico (DFS Secuencial)...")
    res_basic, board_res_basic, met_basic = solver.solve_basic()
    print(f"   -> Resuelto: {res_basic}")
    print(f"   -> Tiempo: {met_basic['tiempo_ms']} ms")
    print(f"   -> Nodos explorados: {met_basic['nodos_explorados']}")
    print(f"   -> Backtracks (retrocesos): {met_basic['backtracks']}")

    print("\n2. Ejecutando Backtracking Optimizado (Heurística MRV + Bitmasks)...")
    res_mrv, board_res_mrv, met_mrv = solver.solve_mrv()
    print(f"   -> Resuelto: {res_mrv}")
    print(f"   -> Tiempo: {met_mrv['tiempo_ms']} ms")
    print(f"   -> Nodos explorados: {met_mrv['nodos_explorados']}")
    print(f"   -> Backtracks (retrocesos): {met_mrv['backtracks']}")

    speedup = met_basic['tiempo_ms'] / max(met_mrv['tiempo_ms'], 0.001)
    prune_pct = (1 - (met_mrv['backtracks'] / max(met_basic['backtracks'], 1))) * 100

    print("\n" + "=" * 70)
    print("ANÁLISIS COMPARATIVO DE RENDIMIENTO (JUSTIFICACIÓN DE COMPLEJIDAD):")
    print(f"• Factor de Aceleración (Speedup): {speedup:.1f}x más rápido con MRV + Bitmasks.")
    print(f"• Reducción de Retrocesos (Poda): MRV redujo los backtracks en un {prune_pct:.2f}%.")
    print("=" * 70)

    print("\n--- TABLERO RESUELTO (VERIFICACIÓN) ---")
    print_board(board_res_mrv, k=3)
