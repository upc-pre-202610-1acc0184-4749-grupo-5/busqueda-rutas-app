import csv


class ConstraintGraph:
    """
    Representa el Sudoku como un grafo de restricciones.

    Cada celda corresponde a un nodo y existe una arista entre
    dos nodos cuando las celdas no pueden contener el mismo valor
    por compartir fila, columna o subcuadro.
    """

    def __init__(self):
        self.adjacency = {}

    def add_node(self, node_id):
        if node_id not in self.adjacency:
            self.adjacency[node_id] = set()

    def add_edge(self, node_a, node_b):
        self.add_node(node_a)
        self.add_node(node_b)

        self.adjacency[node_a].add(node_b)
        self.adjacency[node_b].add(node_a)

    def neighbors(self, node_id):
        return self.adjacency.get(node_id, set())

    def degree(self, node_id):
        return len(self.neighbors(node_id))

    def number_of_nodes(self):
        return len(self.adjacency)

    def number_of_edges(self):
        return sum(
            len(neighbors)
            for neighbors in self.adjacency.values()
        )