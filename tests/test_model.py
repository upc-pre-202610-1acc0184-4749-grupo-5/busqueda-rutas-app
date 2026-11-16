import os
import sys
import unittest

# Ensure src/ is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from model import ConstraintGraph, SudokuBoard


class TestConstraintGraph(unittest.TestCase):
    """Pruebas unitarias para el modelo de grafo de restricciones (Jennifer Riveros)."""

    def test_parametric_dimensions(self):
        """Verifica la generación paramétrica de órdenes k=2, 3, 4 y 7."""
        cases = [
            (2, 4, 16, 7, 56),
            (3, 9, 81, 20, 810),
            (4, 16, 256, 39, 4992),
            (7, 49, 2401, 132, 158466),
        ]
        for k, n, exp_nodes, exp_deg, exp_edges in cases:
            with self.subTest(k=k, n=n):
                graph = ConstraintGraph.build_sudoku(k)
                self.assertEqual(graph.number_of_nodes(), exp_nodes)
                self.assertEqual(graph.number_of_edges(), exp_edges)
                for node_id in range(exp_nodes):
                    self.assertEqual(
                        graph.degree(node_id),
                        exp_deg,
                        f"Fallo en grado del nodo {node_id} para k={k}",
                    )

    def test_dataset_49x49_csv_loading(self):
        """Valida la carga del dataset oficial masivo N=49 (2,401 nodos y 158,466 aristas)."""
        nodes_path = os.path.join(DATASET_DIR, "sudoku_nodes.csv")
        edges_path = os.path.join(DATASET_DIR, "sudoku_edges.csv")

        self.assertTrue(os.path.exists(nodes_path), f"No existe {nodes_path}")
        self.assertTrue(os.path.exists(edges_path), f"No existe {edges_path}")

        graph_csv = ConstraintGraph.from_csv(nodes_path, edges_path)
        self.assertEqual(graph_csv.number_of_nodes(), 2401)
        self.assertEqual(graph_csv.number_of_edges(), 158466)

    def test_structural_identity_build_vs_csv(self):
        """Comprueba que build_sudoku(7) y from_csv generen exactamente la misma topología."""
        nodes_path = os.path.join(DATASET_DIR, "sudoku_nodes.csv")
        edges_path = os.path.join(DATASET_DIR, "sudoku_edges.csv")

        graph_csv = ConstraintGraph.from_csv(nodes_path, edges_path)
        graph_build = ConstraintGraph.build_sudoku(7)

        self.assertEqual(graph_build.adjacency, graph_csv.adjacency)


class TestSudokuBoard(unittest.TestCase):
    """Pruebas unitarias para el estado y validación del tablero SudokuBoard."""

    def test_board_initialization_and_rules(self):
        board = SudokuBoard(k=3)
        self.assertEqual(board.size, 9)
        self.assertEqual(len(board.empty_cells()), 81)
        self.assertTrue(board.is_valid())
        self.assertFalse(board.is_complete())
        self.assertFalse(board.is_solved())

        # Colocar un valor válido
        self.assertTrue(board.set_value(0, 0, 5))
        self.assertEqual(board.get(0, 0), 5)

        # Conflictos en fila, columna y subbloque
        self.assertFalse(board.set_value(0, 1, 5))  # Misma fila
        self.assertFalse(board.set_value(1, 0, 5))  # Misma columna
        self.assertFalse(board.set_value(1, 1, 5))  # Mismo bloque 3x3

        # Colocación válida contigua
        self.assertTrue(board.set_value(0, 1, 6))
        self.assertEqual(board.get(0, 1), 6)

        # Candidatos en celda adyacente
        candidates = board.candidates(0, 2)
        self.assertNotIn(5, candidates)
        self.assertNotIn(6, candidates)
        self.assertIn(1, candidates)


if __name__ == "__main__":
    unittest.main()
