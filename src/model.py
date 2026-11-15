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

    def has_constraint(self, node_a, node_b):
        """
        Indica si existe una restricción entre dos nodos.
        """
        return node_b in self.neighbors(node_a)

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

    @classmethod
    def from_csv(cls, nodes_path, edges_path):
        """
        Crea un grafo nuevo a partir de los archivos CSV del dataset.
        """
        graph = cls()
        graph.load_from_csv(nodes_path, edges_path)
        return graph

    @classmethod
    def build_sudoku(cls, k):
        """
        Construye en memoria el grafo de restricciones de un Sudoku
        de orden k (tablero N x N con N = k^2), sin leer archivos.

        Sirve para tableros de 4x4, 9x9 o 16x16 usados por la GUI,
        mientras que el CSV del dataset contiene el caso N = 49.

        El identificador de cada nodo es fila * N + columna,
        igual que en sudoku_nodes.csv.
        """
        n = k * k
        graph = cls()

        for node_id in range(n * n):
            graph.add_node(node_id)

        for row in range(n):
            for col in range(n):
                node = row * n + col
                block_row = (row // k) * k
                block_col = (col // k) * k

                for i in range(n):
                    if i != col:
                        graph.add_edge(node, row * n + i)
                    if i != row:
                        graph.add_edge(node, i * n + col)

                for r in range(block_row, block_row + k):
                    for c in range(block_col, block_col + k):
                        other = r * n + c
                        if other != node:
                            graph.add_edge(node, other)

        return graph


class SudokuBoard:
    """
    Representa el estado de un tablero de Sudoku de orden k
    (N x N celdas con N = k^2) sobre un ConstraintGraph.

    Los valores se guardan en una lista plana indexada por el
    identificador del nodo (fila * N + columna). Las reglas del
    juego no se revisan recorriendo filas, columnas y subcuadros,
    sino consultando los vecinos de la celda en el grafo:
    una asignación es válida si ningún vecino tiene el mismo valor.

    El valor 0 representa una celda vacía.
    """

    EMPTY = 0

    def __init__(self, k=3, graph=None):
        self.k = k
        self.size = k * k

        if graph is None:
            graph = ConstraintGraph.build_sudoku(k)

        expected_nodes = self.size * self.size
        if graph.number_of_nodes() != expected_nodes:
            raise ValueError(
                f"El grafo tiene {graph.number_of_nodes()} nodos, "
                f"pero un tablero {self.size}x{self.size} "
                f"necesita {expected_nodes}."
            )

        self.graph = graph
        self.values = [self.EMPTY] * expected_nodes
        self.fixed = set()

    # ------------------------------------------------------------------
    # Conversión entre coordenadas y nodos
    # ------------------------------------------------------------------
    def node_id(self, row, col):
        """
        Convierte una posición (fila, columna) en el id del nodo.
        """
        self._check_position(row, col)
        return row * self.size + col

    def position(self, node_id):
        """
        Convierte el id de un nodo en su posición (fila, columna).
        """
        return divmod(node_id, self.size)

    def _check_position(self, row, col):
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(
                f"La posición ({row}, {col}) está fuera del tablero "
                f"{self.size}x{self.size}."
            )

    def _check_value(self, value):
        if not isinstance(value, int) or not (0 <= value <= self.size):
            raise ValueError(
                f"El valor {value!r} no es válido: debe ser un entero "
                f"entre 1 y {self.size} (o 0 para vaciar la celda)."
            )

    # ------------------------------------------------------------------
    # Inicialización de pistas
    # ------------------------------------------------------------------
    @classmethod
    def from_matrix(cls, matrix, k=None, graph=None):
        """
        Crea un tablero a partir de una matriz N x N (lista de listas).
        Los valores distintos de 0 se cargan como pistas fijas.

        Si no se indica k, se deduce del tamaño de la matriz.
        """
        if k is None:
            k = int(round(len(matrix) ** 0.5))

        board = cls(k, graph)
        board.load_clues(matrix)
        return board

    def load_clues(self, matrix):
        """
        Carga las pistas iniciales desde una matriz N x N.

        Valida que la matriz tenga el tamaño correcto, que cada valor
        esté en el rango permitido y que las pistas no se contradigan
        entre sí. Si algo falla, el tablero queda sin cambios.
        """
        if len(matrix) != self.size or any(
            len(row) != self.size for row in matrix
        ):
            raise ValueError(
                f"La matriz debe ser de {self.size}x{self.size}."
            )

        new_values = [self.EMPTY] * (self.size * self.size)
        new_fixed = set()

        for row in range(self.size):
            for col in range(self.size):
                value = matrix[row][col]
                self._check_value(value)
                if value != self.EMPTY:
                    node = row * self.size + col
                    new_values[node] = value
                    new_fixed.add(node)

        conflicts = self._find_conflicts(new_values)
        if conflicts:
            (a, b) = conflicts[0]
            raise ValueError(
                "Las pistas iniciales se contradicen: las celdas "
                f"{self.position(a)} y {self.position(b)} tienen "
                f"el valor {new_values[a]}."
            )

        self.values = new_values
        self.fixed = new_fixed

    def to_matrix(self):
        """
        Devuelve el tablero como matriz N x N (lista de listas),
        el formato que usan SudokuSolver y la GUI.
        """
        return [
            self.values[row * self.size:(row + 1) * self.size]
            for row in range(self.size)
        ]

    # ------------------------------------------------------------------
    # Lectura y escritura de celdas
    # ------------------------------------------------------------------
    def get(self, row, col):
        return self.values[self.node_id(row, col)]

    def is_fixed(self, row, col):
        """
        Indica si la celda es una pista inicial (no editable).
        """
        return self.node_id(row, col) in self.fixed

    def set_value(self, row, col, value):
        """
        Asigna un valor a una celda editable si respeta las reglas.

        Devuelve True si se asignó y False si el valor choca con
        algún vecino del grafo. Lanza un error si la celda es una
        pista fija o si el valor está fuera de rango.
        """
        self._check_value(value)
        node = self.node_id(row, col)

        if node in self.fixed:
            raise ValueError(
                f"La celda ({row}, {col}) es una pista inicial "
                "y no se puede modificar."
            )

        if value != self.EMPTY and not self.is_valid_move(row, col, value):
            return False

        self.values[node] = value
        return True

    def clear(self, row, col):
        """
        Vacía una celda editable.
        """
        self.set_value(row, col, self.EMPTY)

    def reset(self):
        """
        Borra todos los valores ingresados, conservando las pistas.
        """
        for node in range(len(self.values)):
            if node not in self.fixed:
                self.values[node] = self.EMPTY

    # ------------------------------------------------------------------
    # Validación de reglas usando el grafo de restricciones
    # ------------------------------------------------------------------
    def is_valid_move(self, row, col, value):
        """
        Indica si se puede colocar 'value' en (row, col).

        Recorre solo los vecinos del nodo en el grafo: O(grado),
        es decir 3N - 2k - 1 restricciones por celda.
        """
        node = self.node_id(row, col)
        return all(
            self.values[neighbor] != value
            for neighbor in self.graph.neighbors(node)
        )

    def candidates(self, row, col):
        """
        Devuelve los valores que todavía se pueden colocar en la
        celda (su dominio), descartando los usados por sus vecinos.
        Si la celda ya tiene valor, devuelve una lista vacía.
        """
        node = self.node_id(row, col)
        if self.values[node] != self.EMPTY:
            return []

        used = {
            self.values[neighbor]
            for neighbor in self.graph.neighbors(node)
        }
        return [
            value for value in range(1, self.size + 1)
            if value not in used
        ]

    def _find_conflicts(self, values):
        conflicts = []
        for node, neighbors in self.graph.adjacency.items():
            value = values[node]
            if value == self.EMPTY:
                continue
            for neighbor in neighbors:
                if node < neighbor and values[neighbor] == value:
                    conflicts.append((node, neighbor))
        return conflicts

    def conflicts(self):
        """
        Devuelve las restricciones violadas como pares de posiciones
        ((fila_a, col_a), (fila_b, col_b)) con el mismo valor.
        """
        return [
            (self.position(a), self.position(b))
            for a, b in self._find_conflicts(self.values)
        ]

    def empty_cells(self):
        """
        Devuelve las posiciones (fila, columna) de las celdas vacías.
        """
        return [
            self.position(node)
            for node, value in enumerate(self.values)
            if value == self.EMPTY
        ]

    def is_valid(self):
        """
        True si ninguna restricción está violada (puede haber vacías).
        """
        return not self._find_conflicts(self.values)

    def is_complete(self):
        """
        True si no queda ninguna celda vacía.
        """
        return self.EMPTY not in self.values

    def is_solved(self):
        """
        True si el tablero está completo y respeta todas las reglas.
        """
        return self.is_complete() and self.is_valid()

    def __str__(self):
        width = len(str(self.size))
        lines = []
        for row in range(self.size):
            if row and row % self.k == 0:
                lines.append("")
            cells = []
            for col in range(self.size):
                if col and col % self.k == 0:
                    cells.append("|")
                value = self.get(row, col)
                cells.append(str(value).rjust(width) if value else ".".rjust(width))
            lines.append(" ".join(cells))
        return "\n".join(lines)