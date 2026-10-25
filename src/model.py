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
        """
        Agrega un nodo al grafo si todavía no existe.
        """
        if node_id not in self.adjacency:
            self.adjacency[node_id] = set()

    def add_edge(self, node_a, node_b):
        """
        Agrega una restricción entre dos nodos.

        Como las restricciones del Sudoku son bidireccionales,
        la arista se almacena en ambos sentidos.
        """
        self.add_node(node_a)
        self.add_node(node_b)

        self.adjacency[node_a].add(node_b)
        self.adjacency[node_b].add(node_a)

    def neighbors(self, node_id):
        """
        Devuelve las celdas que tienen una restricción
        con el nodo indicado.
        """
        return self.adjacency.get(node_id, set())

    def degree(self, node_id):
        """
        Devuelve la cantidad de restricciones de un nodo.
        """
        return len(self.neighbors(node_id))

    def number_of_nodes(self):
        """
        Devuelve la cantidad total de nodos cargados.
        """
        return len(self.adjacency)

    def number_of_edges(self):
        """
        Devuelve la cantidad total de aristas.

        Cada arista se almacena dos veces en la lista de
        adyacencia, por eso se divide entre 2.
        """
        total = sum(
            len(neighbors)
            for neighbors in self.adjacency.values()
        )

        return total // 2

    def load_nodes(self, filepath):
        """
        Carga los nodos desde sudoku_nodes.csv.
        """
        with open(
            filepath,
            mode="r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                node_id = int(row["node_id"])
                self.add_node(node_id)

    def load_edges(self, filepath):
        """
        Carga las restricciones desde sudoku_edges.csv.
        """
        with open(
            filepath,
            mode="r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                origin = int(row["origen"])
                destination = int(row["destino"])

                self.add_edge(origin, destination)

    def load_from_csv(self, nodes_path, edges_path):
        """
        Carga primero los nodos y luego todas las restricciones.
        """
        self.load_nodes(nodes_path)
        self.load_edges(edges_path)