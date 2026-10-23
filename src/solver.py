"""
solver.py
=========
Módulo de Algoritmia y Complejidad para la resolución de Sudokus Generalizados N x N.
Desarrollado para el Hito 2 (TB2) - Complejidad Algorítmica (CC184).
Autor: Pareja Calloapaza, Marcelo Fausto (u202411627)

Presenta una arquitectura comparativa con 3 niveles evolutivos de optimización:
  Nivel 1: Backtracking Básico (Búsqueda en Profundidad / DFS Secuencial)
  Nivel 2: Backtracking con Heurística MRV Clásica (Minimum Remaining Values / "Fallar Primero")
  Nivel 3: Backtracking con Heurística MRV + Poda por Máscaras de Bits (Bitmasks en O(1))
"""

import time
import copy
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
        
        # Métricas de rendimiento
        self.backtracks = 0
        self.nodes_explored = 0
        self.execution_time = 0.0

    # =========================================================================
    # REGLAS DEL JUEGO / VALIDACIÓN DE RESTRICCIONES DE ARISTA (O(N))
    # =========================================================================
    def es_movimiento_valido(self, board: List[List[int]], fila: int, col: int, numero: int) -> bool:
        """
        Verifica si la asignación es legal respecto a las aristas del grafo:
        1. Fila
        2. Columna
        3. Subbloque k x k
        """
        # 1. Comprobar fila
        for c in range(self.N):
            if board[fila][c] == numero:
                return False

        # 2. Comprobar columna
        for f in range(self.N):
            if board[f][col] == numero:
                return False

        # 3. Comprobar subbloque k x k
        inicio_fila = (fila // self.k) * self.k
        inicio_col = (col // self.k) * self.k
        for ifil in range(inicio_fila, inicio_fila + self.k):
            for icol in range(inicio_col, inicio_col + self.k):
                if board[ifil][icol] == numero:
                    return False

        return True

    # =========================================================================
    # NIVEL 1: BACKTRACKING BÁSICO (DFS SECUENCIAL)
    # =========================================================================
    def resolver_basico(self) -> Tuple[bool, List[List[int]], Dict]:
        """
        Resuelve mediante Backtracking tradicional explorando celdas
        en orden secuencial de lectura.
        """
        self.backtracks = 0
        self.nodes_explored = 0
        start_time = time.perf_counter()

        tablero = [row[:] for row in self.board]
        exito = self._backtrack_basico(tablero)

        self.execution_time = (time.perf_counter() - start_time) * 1000

        metricas = {
            "estrategia": "Nivel 1: Backtracking Básico (DFS Secuencial)",
            "resuelto": exito,
            "tiempo_ms": round(self.execution_time, 3),
            "nodos_explorados": self.nodes_explored,
            "backtracks": self.backtracks
        }
        return exito, tablero, metricas

    def _encontrar_vacia_secuencial(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        for c in range(self.N):
            for f in range(self.N):
                if board[f][c] == 0:
                    return f, c
        return None

    def _backtrack_basico(self, board: List[List[int]]) -> bool:
        celda = self._encontrar_vacia_secuencial(board)
        if celda is None:
            return True  # Tablero completo

        fila, col = celda
        for num in range(1, self.N + 1):
            self.nodes_explored += 1
            if self.es_movimiento_valido(board, fila, col, num):
                board[fila][col] = num
                if self._backtrack_basico(board):
                    return True
                # Vuelta atrás
                board[fila][col] = 0
                self.backtracks += 1

        return False

    # =========================================================================
    # NIVEL 2: BACKTRACKING CON HEURÍSTICA MRV CLÁSICA (DOMINIOS EN LISTAS)
    # =========================================================================
    def resolver_mrv_clasico(self) -> Tuple[bool, List[List[int]], Dict]:
        """
        Resuelve mediante Backtracking con heurística MRV (Minimum Remaining Values),
        calculando los candidatos legales con listas iterativas y aplicando poda inmediata.
        """
        self.backtracks = 0
        self.nodes_explored = 0
        start_time = time.perf_counter()

        tablero = [row[:] for row in self.board]
        exito = self._backtrack_mrv_clasico(tablero)

        self.execution_time = (time.perf_counter() - start_time) * 1000

        metricas = {
            "estrategia": "Nivel 2: Backtracking con Heurística MRV Clásica",
            "resuelto": exito,
            "tiempo_ms": round(self.execution_time, 3),
            "nodos_explorados": self.nodes_explored,
            "backtracks": self.backtracks
        }
        return exito, tablero, metricas

    def _obtener_valores_legales(self, board: List[List[int]], fila: int, col: int) -> List[int]:
        candidatos = []
        for i in range(self.N):
            val = i + 1
            if self.es_movimiento_valido(board, fila, col, val):
                candidatos.append(val)
        return candidatos

    def _encontrar_celda_mrv_clasica(self, board: List[List[int]]) -> Optional[Tuple[int, int, List[int]]]:
        menor_cantidad = self.N + 1
        mejor_celda = None

        for f in range(self.N):
            for c in range(self.N):
                if board[f][c] == 0:
                    candidatos = self._obtener_valores_legales(board, f, c)
                    cantidad = len(candidatos)

                    # Poda inmediata (callejón sin salida)
                    if cantidad == 0:
                        return f, c, []

                    if cantidad < menor_cantidad:
                        menor_cantidad = cantidad
                        mejor_celda = (f, c, candidatos)
                        if menor_cantidad == 1:
                            return mejor_celda  # Singleton óptimo

        return mejor_celda

    def _backtrack_mrv_clasico(self, board: List[List[int]]) -> bool:
        celda = self._encontrar_celda_mrv_clasica(board)
        if celda is None:
            return True  # Tablero completo

        fila, col, candidatos = celda

        # Si el dominio es vacío, podamos la rama
        if len(candidatos) == 0:
            self.backtracks += 1
            return False

        for cand in candidatos:
            self.nodes_explored += 1
            board[fila][col] = cand

            if self._backtrack_mrv_clasico(board):
                return True

            # Vuelta atrás
            board[fila][col] = 0
            self.backtracks += 1

        return False

    # =========================================================================
    # NIVEL 3: BACKTRACKING CON HEURÍSTICA MRV + MÁSCARAS DE BITS (BITMASKS O(1))
    # =========================================================================
    def resolver_mrv_bitmasks(self) -> Tuple[bool, List[List[int]], Dict]:
        """
        Resuelve mediante Backtracking con MRV utilizando máscaras de bits binarias.
        Reduce las comprobaciones de fila, columna y bloque a operaciones bitwise O(1).
        """
        self.backtracks = 0
        self.nodes_explored = 0
        start_time = time.perf_counter()

        tablero = [row[:] for row in self.board]

        row_masks = [0] * self.N
        col_masks = [0] * self.N
        box_masks = [0] * self.N
        empty_cells = []

        for r in range(self.N):
            for c in range(self.N):
                val = tablero[r][c]
                if val != 0:
                    bit = 1 << val
                    row_masks[r] |= bit
                    col_masks[c] |= bit
                    box_masks[(r // self.k) * self.k + (c // self.k)] |= bit
                else:
                    empty_cells.append((r, c))

        all_mask = (1 << (self.N + 1)) - 2

        exito = self._backtrack_mrv_bitmasks_core(tablero, empty_cells, row_masks, col_masks, box_masks, all_mask)

        self.execution_time = (time.perf_counter() - start_time) * 1000

        metricas = {
            "estrategia": "Nivel 3: Backtracking con Heurística MRV + Bitmasks O(1)",
            "resuelto": exito,
            "tiempo_ms": round(self.execution_time, 3),
            "nodos_explorados": self.nodes_explored,
            "backtracks": self.backtracks
        }
        return exito, tablero, metricas

    def _backtrack_mrv_bitmasks_core(self, board, empty_cells, row_masks, col_masks, box_masks, all_mask) -> bool:
        if not empty_cells:
            return True

        best_idx = -1
        best_candidates_mask = 0
        min_count = self.N + 2

        for i, (r, c) in enumerate(empty_cells):
            b_idx = (r // self.k) * self.k + (c // self.k)
            used = row_masks[r] | col_masks[c] | box_masks[b_idx]
            avail = all_mask & (~used)
            count = avail.bit_count()

            # Poda inmediata
            if count == 0:
                self.backtracks += 1
                return False

            if count < min_count:
                min_count = count
                best_idx = i
                best_candidates_mask = avail
                if count == 1:
                    break

        r, c = empty_cells.pop(best_idx)
        b_idx = (r // self.k) * self.k + (c // self.k)

        mask = best_candidates_mask
        while mask > 0:
            lowest_bit = mask & (-mask)
            val = lowest_bit.bit_length() - 1

            self.nodes_explored += 1
            board[r][c] = val
            row_masks[r] |= lowest_bit
            col_masks[c] |= lowest_bit
            box_masks[b_idx] |= lowest_bit

            if self._backtrack_mrv_bitmasks_core(board, empty_cells, row_masks, col_masks, box_masks, all_mask):
                return True

            board[r][c] = 0
            row_masks[r] &= ~lowest_bit
            col_masks[c] &= ~lowest_bit
            box_masks[b_idx] &= ~lowest_bit
            self.backtracks += 1

            mask &= ~lowest_bit

        empty_cells.insert(best_idx, (r, c))
        return False


def imprimir_tablero(board: List[List[int]], k: int = 3):
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


# =========================================================================
# BANCO DE PRUEBAS COMPARATIVO (BENCHMARK)
# =========================================================================
if __name__ == "__main__":
    print("=" * 75)
    print("MODULO DE ALGORITMIA: BENCHMARKING DE RESOLUCION DE SUDOKU")
    print("Autor: Pareja Calloapaza, Marcelo Fausto (u202411627)")
    print("=" * 75)

    tablero_dificil = [
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

    print("\n--- TABLERO DE PRUEBA (Dificultad Alta: 17 pistas iniciales) ---")
    imprimir_tablero(tablero_dificil, k=3)

    solver = SudokuSolver(tablero_dificil, k=3)

    # 1. Nivel 1: Básico
    print("\n[1/3] Ejecutando Nivel 1: Backtracking Basico (DFS Secuencial)...")
    res1, board1, met1 = solver.resolver_basico()
    print(f"      -> Resuelto: {res1} | Tiempo: {met1['tiempo_ms']:.2f} ms | Backtracks: {met1['backtracks']:,}")

    # 2. Nivel 2: MRV Clásico (Tu algoritmo con listas)
    print("\n[2/3] Ejecutando Nivel 2: Backtracking con Heuristica MRV Clasica...")
    res2, board2, met2 = solver.resolver_mrv_clasico()
    print(f"      -> Resuelto: {res2} | Tiempo: {met2['tiempo_ms']:.2f} ms | Backtracks: {met2['backtracks']:,}")

    # 3. Nivel 3: MRV con Bitmasks (Optimización de bajo nivel)
    print("\n[3/3] Ejecutando Nivel 3: Backtracking con Heuristica MRV + Bitmasks O(1)...")
    res3, board3, met3 = solver.resolver_mrv_bitmasks()
    print(f"      -> Resuelto: {res3} | Tiempo: {met3['tiempo_ms']:.2f} ms | Backtracks: {met3['backtracks']:,}")

    print("\n--- TABLERO RESUELTO (VERIFICACION FINAL) ---")
    imprimir_tablero(board3, k=3)

    print("\n" + "=" * 75)
    print("CUADRO COMPARATIVO FINAL DE COMPLEJIDAD Y RENDIMIENTO")
    print("=" * 75)
    print(f"{'Estrategia':<40} | {'Tiempo (ms)':<12} | {'Backtracks':<12} | {'Poda':<10}")
    print("-" * 75)
    poda_mrv = ((met1['backtracks'] - met2['backtracks']) / met1['backtracks']) * 100
    print(f"{met1['estrategia']:<40} | {met1['tiempo_ms']:>10.2f} ms | {met1['backtracks']:>12,} | {'Linea base':<10}")
    print(f"{met2['estrategia']:<40} | {met2['tiempo_ms']:>10.2f} ms | {met2['backtracks']:>12,} | {f'-{poda_mrv:.2f}%':<10}")
    print(f"{met3['estrategia']:<40} | {met3['tiempo_ms']:>10.2f} ms | {met3['backtracks']:>12,} | {f'-{poda_mrv:.2f}%':<10}")
    print("=" * 75)

    speedup_total = met1['tiempo_ms'] / max(met3['tiempo_ms'], 0.001)
    print(f"FACTOR DE ACELERACION GLOBAL (Nivel 1 vs Nivel 3): {speedup_total:.1f}x mas rapido")
    print("=" * 75)
