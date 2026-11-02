from tkinter import *
from tkinter import messagebox
import tkinter as tk
import random
import pandas as pd
import os
import sys

from solver import SudokuSolver

# App Info
AppName = "Sudoku Studio"
AppDescription = "NxN Sudoku Puzzle Generator and Solver. Motor de Heuristica con Backtracking y Poda (CSP) - CC184"
version = "1.0.0"

# Main Window
main_window = Tk()
main_window.title(AppName + " v" + version)
main_window.geometry("1000x1000")

UserColor = "#5938C4"
AlgorithmColor = "#d29bfd"
ProgramColor = "#000000"
ErrorColor = "#DC143C"

Cells = 0
Edges = 0

Backtracks = 0
State = 0

Timer_Switch = False
Timer = 0

StateVal = {
    "Solved": None
}

current_settings = {
    "Dimension": None,
    "Difficulty": None,
    "Algorithm": None

}

GridSizeVar = {None}
GridSizeVar = StringVar()
GridTextVar = {None}
GridTextVar = StringVar()
StateTextVar = {None}
StateTextVar = StringVar()

BacktrackingTextVar = StringVar()

BoardFrame  = None

entries = {}

def validate_numeric_input(P):
    """
    Returns True if the input value is a number or empty (allows deletion).
    Blocks letters and special characters automatically.
    """
    if P == "":
        return True
    if P.isdigit():
        val = int(P)
        
        # Obtain the maximum size (N) based on the current dimension
        grid_size_str = GridSizeVar.get()
        if "4x4" in grid_size_str:
            max_val = 4
        elif "16x16" in grid_size_str:
            max_val = 16
        else:
            max_val = 9  # Default 9x9 (Classic)
            
        # Allow only numbers from 1 to N (adapts if it's 4x4, 9x9 or 16x16)
        if 1 <= val <= max_val:
            return True
        
    return False

def SaveSetting(*args):
    global Cells, Edges, BoardFrame

    current_settings["Dimension"] = DimensionVar.get()
    current_settings["Difficulty"] = DifficultyVar.get()
    current_settings["Algorithm"] = AlgorithmVar.get()

    if DimensionVar.get() == "4x4 (K=2) [Small]":
        current_settings["Dimension"] = "4x4"
        Cells = 16
        Edges = 56
    elif DimensionVar.get() == "9x9 (K=3) [Classic]":
        current_settings["Dimension"] = "9x9"
        Cells = 81
        Edges = 810
    elif DimensionVar.get() == "16x16 (K=4) [Large]":
        current_settings["Dimension"] = "16x16"
        Cells = 256
        Edges = 4992
    else:
        current_settings["Dimension"] = "error"
        Cells = 0
        Edges = 0

    GridSizeVar.set(f" {current_settings['Dimension']}")
    GridTextVar.set(f"Cuadrícula: {GridSizeVar.get()} ({Cells} Celdas {Edges} Aristas)")

    State_Val()

    if BoardFrame is not None:
        DrawGrid(BoardFrame, GridSizeVar.get())

def State_Val():
    global State
    if State == 1:
        StateVal["Solved"] = "resuelto con exito"
    elif State == 2:
        StateVal["Solved"] = "resuelto, pero incorrecto"
    elif State == 0:
        StateVal["Solved"] = "no resuelto"
    else:
        State = 0
        StateVal["Solved"] = "no resuelto"
        
    StateTextVar.set(f"Estado: Sudoku {GridSizeVar.get()} {StateVal['Solved']}")

def DrawGrid_in_Frame(Frame_Container, size):
    global entries
    
    for widget in Frame_Container.winfo_children():
        widget.destroy()
        
    entries.clear()

    sub_size = int(size**0.5)

    if size == 16:
        font_size = 9
        entry_width = 2
        pad_space = 0
    elif size == 9:
        font_size = 11
        entry_width = 2
        pad_space = 1
    else: # 4x4
        font_size = 11
        entry_width = 2
        pad_space = 2

    outer_frame = tk.Frame(Frame_Container, bg="white", bd=2)
    outer_frame.pack(padx=2, pady=2)

    board_inner_frame = tk.Frame(outer_frame, bg="black", bd=2)
    board_inner_frame.pack(padx=1, pady=1)

    boxes = {}
    for br in range(sub_size):
        for bc in range(sub_size):
            box = tk.Frame(board_inner_frame, bg="black", bd=1)
            box.grid(row=br, column=bc, padx=pad_space, pady=pad_space)
            boxes[(br, bc)] = box

    vcmd = (Frame_Container.register(validate_numeric_input), '%P')

    for r in range(size):
        for c in range(size):
            br, bc = r // sub_size, c // sub_size
            lr, lc = r % sub_size, c % sub_size

            entry = tk.Entry(
                boxes[(br, bc)], 
                width=entry_width, 
                font=("Arial", font_size, "bold"), 
                justify="center",
                bg="white",      
                fg="black",      
                insertbackground="black",
                relief="flat",
                validate="key",   
                validatecommand=vcmd
            )
            
            entry.grid(row=lr, column=lc, padx=1, pady=1)
            entries[(r, c)] = entry

def Draw4x4Grid(Frame):
    DrawGrid_in_Frame(Frame, 4)

def Draw9x9Grid(Frame):
    DrawGrid_in_Frame(Frame, 9)

def Draw16x16Grid(Frame):
    DrawGrid_in_Frame(Frame, 16)

def DrawGrid(Frame, GridSize):
    GridSize = GridSizeVar.get()
    if "4x4" in GridSize:
        Draw4x4Grid(Frame)
    elif "9x9" in GridSize:
        Draw9x9Grid(Frame)
    elif "16x16" in GridSize:
        Draw16x16Grid(Frame)
    else:
        messagebox.showerror("Error de Dimension", "La dimension no coincide")

def fill_cells_by_percentage(size, entries, board_solution, fill_percentage):
    """
    Randomly fills the initial clues based on difficulty percentage
    and updates both the GUI entries and the grid graph/model.
    """
    total_cells = size * size
    num_clues = int(total_cells * fill_percentage)
    
    all_positions = [(r, c) for r in range(size) for c in range(size)]
    clue_positions = set(random.sample(all_positions, num_clues))
    
    for r in range(size):
        for c in range(size):
            entry = entries.get((r, c))
            if entry is None:
                continue
                
            # 1. Enable the entry to allow insertion and set default colors
            entry.config(state="normal", fg=ProgramColor, bg="white")
            # 2. erease any existing value before inserting new one
            entry.delete(0, tk.END)
            
            if (r, c) in clue_positions:
                value = str(board_solution[r][c])
                entry.insert(0, value)
                # Block the cell as readonly for program-generated clues
                entry.config(state="readonly", readonlybackground="white", fg=ProgramColor)
            else:
                # empty cell for user input
                entry.config(state="normal", bg="white", fg=UserColor)

def set_values_easy(size, entries, board_solution):
    fill_cells_by_percentage(size, entries, board_solution, fill_percentage=0.55)

def set_values_medium(size, entries, board_solution):
    fill_cells_by_percentage(size, entries, board_solution, fill_percentage=0.40)

def set_values_hard(size, entries, board_solution):
    fill_cells_by_percentage(size, entries, board_solution, fill_percentage=0.25)

def set_values_expert(size, entries, board_solution):
    fill_cells_by_percentage(size, entries, board_solution, fill_percentage=0.20)

def generate_valid_base_board(size):
    """
    Generates a randomized valid solved base board matrix for the given size 
    by shuffling rows, columns, and numbers while preserving Sudoku constraints.
    """
    sub_size = int(size ** 0.5)
    
    board = [[0] * size for _ in range(size)]
    for r in range(size):
        for c in range(size):
            board[r][c] = (sub_size * (r % sub_size) + r // sub_size + c) % size + 1

    nums = list(range(1, size + 1))
    random.shuffle(nums)
    board = [[nums[val - 1] for val in row] for row in board]

    for b in range(sub_size):
        row_indices = list(range(b * sub_size, (b + 1) * sub_size))
        random.shuffle(row_indices)
        board = [board[i] for i in row_indices] + [board[i] for i in range(len(board)) if i not in row_indices]

    def shuffle_bands(b):
        nonlocal board
        for blk in range(sub_size):
            start = blk * sub_size
            band = board[start:start+sub_size]
            random.shuffle(band)
            board[start:start+sub_size] = band

    shuffle_bands(sub_size)
    
    def shuffle_stacks(b):
        nonlocal board
        for blk in range(sub_size):
            start = blk * sub_size
            transposed = [list(x) for x in zip(*board)]
            stack = transposed[start:start+sub_size]
            random.shuffle(stack)
            transposed[start:start+sub_size] = stack
            board = [list(x) for x in zip(*transposed)]

    shuffle_stacks(sub_size)

    return board

def set_values(entries):
    """
    Master function that reads the difficulty, determines grid size (k),
    reads nodes/edges datasets, and populates the grid.
    """
    # 1. Get current grid size from interface settings
    grid_size_str = GridSizeVar.get()
    if "4x4" in grid_size_str:
        size = 4
        k = 2
    elif "9x9" in grid_size_str:
        size = 9
        k = 3
    elif "16x16" in grid_size_str:
        size = 16
        k = 4
    else:
        size = 9
        k = 3

    # 2. Read dataset files (sudoku_nodes.csv and sudoku_edges.csv)
    nodes_path = "../dataset/sudoku_nodes.csv"
    edges_path = "../dataset/sudoku_edges.csv"

    if os.path.exists(nodes_path) and os.path.exists(edges_path):
        nodes_df = pd.read_csv(nodes_path)
        edges_df = pd.read_csv(edges_path)
        print(f"Dataset loaded: {len(nodes_df)} nodes and {len(edges_df)} edges found for k={k}.")
    else:
        print("Warning: Dataset CSV files not found. Ensure the graph generator has run.")

    # 3. Get current difficulty level
    difficulty = DifficultyVar.get()

    # 4. Generate or fetch a valid board solution matrix for the given size
    # (You can map this to your base solution generator function)
    board_solution = generate_valid_base_board(size) 

    # 5. Route to the correct difficulty setter function based on percentages
    if "Fácil (45% Vacio)" in difficulty:
        set_values_easy(size, entries, board_solution)
    elif "Medio (60% Vacio)" in difficulty:
        set_values_medium(size, entries, board_solution)
    elif "Difícil (75% Vacio)" in difficulty:
        set_values_hard(size, entries, board_solution)
    elif "Experto (80% Vacio)" in difficulty:
        set_values_expert(size, entries, board_solution)
    else:
        set_values_easy(size, entries, board_solution)

def validate_sudoku_solution():
    global State
    print("--- Executing validate_sudoku_solution ---")
    
    grid_size_str = GridSizeVar.get()
    if "4x4" in grid_size_str:
        size = 4
    elif "9x9" in grid_size_str:
        size = 9
    elif "16x16" in grid_size_str:
        size = 16
    else:
        size = 9

    N = size
    current_dir = os.path.dirname(os.path.abspath(__file__))
    edges_path = os.path.join(current_dir, "../dataset/sudoku_edges.csv")
    
    if not os.path.exists(edges_path):
        print(f"Error: The file does not exist at {edges_path}")
        return

    edges_df = pd.read_csv(edges_path)
    print(f"Edges Loaded: {len(edges_df)}")

    board_values = {}
    is_incomplete = False

    for r in range(size):
        for c in range(size):
            node_id = r * N + c
            entry = entries.get((r, c))
            val_str = entry.get().strip() if entry else ""
            if val_str.isdigit():
                board_values[node_id] = int(val_str)
                if val_str == "0":
                    is_incomplete = True
            else:
                board_values[node_id] = None
                is_incomplete = True
    if is_incomplete:
        messagebox.showwarning("Tablero Incompleto", "El Sudoku no está completo. Rellena todas las celdas antes de enviar.")
        return
    
    is_valid = True
    for _, row in edges_df.iterrows():
        u = int(row['origen'])
        v = int(row['destino'])
        
        if u in board_values and v in board_values:
            val_u = board_values.get(u)
            val_v = board_values.get(v)
            
            if val_u is None or val_v is None or val_u == val_v:
                is_valid = False
                break

    print(f"Validation's results (is_valid): {is_valid}")

    if is_valid:
        State = 1  # Solved correctly
    else:
        State = 2  # Solved incorrectly

    print(f"New State assigned value: {State}")
    State_Val()

def read_current_board_from_gui(size):
    """
    Reads the current values from the GUI entry widgets 
    and builds a 2D matrix representing the board.
    """
    board = [[0] * size for _ in range(size)]
    for r in range(size):
        for c in range(size):
            entry = entries.get((r, c))
            if entry:
                val_str = entry.get().strip()
                if val_str.isdigit():
                    board[r][c] = int(val_str)
                else:
                    board[r][c] = 0
    return board

def update_gui_with_solved_board(original_board, solved_board, size):
    """
    Updates the GUI entry widgets with the solved board matrix 
    and locks them or marks them appropriately.
    """
    for r in range(size):
        for c in range(size):
            entry = entries.get((r, c))
            if entry:
                # Enable temporarily to insert value
                entry.config(state="normal")
                original_val = original_board[r][c]
                solved_val = solved_board[r][c]

                entry.delete(0, tk.END)

                if solved_val != 0:
                    entry.insert(0, str(solved_val))

                    if original_val != 0:
                        entry.config(state="readonly", readonlybackground="white", fg=ProgramColor)
                    else:
                        # Lock resolved cells as readonly
                        entry.config(state="readonly", readonlybackground="white", fg=AlgorithmColor)
                else:
                    entry.config(state="normal", bg="white", fg=ProgramColor)

def solve_sudoku_from_interface():
    """
    Solves the Sudoku using the selected algorithm from solver.py,
    updates global telemetry variables (Backtracks, Timer, State),
    and redraws the solution on the screen.
    """
    global State, Backtracks  
    
    grid_size_str = GridSizeVar.get()
    if "4x4" in grid_size_str:
        size = 4
        k = 2
    elif "9x9" in grid_size_str:
        size = 9
        k = 3
    elif "16x16" in grid_size_str:
        size = 16
        k = 4
    else:
        size = 9
        k = 3

    current_board = read_current_board_from_gui(size)
    solver = SudokuSolver(current_board, k=k)
    selected_algorithm = AlgorithmVar.get() if 'AlgorithmVar' in globals() else "Nivel 1"

    if "Nivel 1" in selected_algorithm or "Básico" in selected_algorithm:
        success, solved_board, metrics = solver.resolver_basico()
    elif "Nivel 2" in selected_algorithm or "MRV Clásica" in selected_algorithm:
        success, solved_board, metrics = solver.resolver_mrv_clasico()
    elif "Nivel 3" in selected_algorithm or "Bitmasks" in selected_algorithm:
        success, solved_board, metrics = solver.resolver_mrv_bitmasks()
    else:
        success, solved_board, metrics = solver.resolver_mrv_bitmasks()

    # Actualizar métricas globales de rendimiento
    Backtracks = metrics["backtracks"]
    execution_time_ms = metrics["tiempo_ms"]

    if 'Timer_Switch' in globals():
        global Timer_Switch
        Timer_Switch = False  

    # Actualizar texto del Timer en la interfaz
    if 'TimeLabel' in globals():
        TimeLabel.config(text=f"Tiempo: {execution_time_ms:.2f} ms")

    # Actualizar texto de Backtracks correctamente usando StringVar
    BacktrackingTextVar.set(f"Retrocesos(Backtracking): {Backtracks:,}")

    if success:
        State = 1  
    else:
        State = 2  

    if success:
        update_gui_with_solved_board(current_board, solved_board, size)

    if 'State_Val' in globals():
        State_Val()

    print(f"Solver executed via {metrics['estrategia']}. Success: {success}, Time: {execution_time_ms} ms, Backtracks: {Backtracks}")
    return success, metrics

def open_custom_sudoku_window():
    """
    Opens a new Toplevel window containing an empty grid for the user 
    to input their own custom puzzle. Validates row/column constraints 
    before copying valid entries to the main board.
    """
    global entries, GridSizeVar
    
    # 1. Determine current grid size
    grid_size_str = GridSizeVar.get()
    if "4x4" in grid_size_str:
        size = 4
    elif "9x9" in grid_size_str:
        size = 9
    elif "16x16" in grid_size_str:
        size = 16
    else:
        size = 9

    sub_size = int(size**0.5)

    # 2. Create Toplevel Window
    custom_window = tk.Toplevel(main_window)
    custom_window.title("Crear mi propio Sudoku")
    custom_window.geometry("500x550")
    custom_window.config(bg="white")

    title_label = Label(custom_window, text="Diseña tu propio Sudoku", font=("Arial", 12, "bold"), bg="white")
    title_label.pack(pady=10)

    # 3. Frame container for the custom grid
    custom_frame = tk.Frame(custom_window, bg="white")
    custom_frame.pack(pady=5)

    custom_entries = {}

    # Rendering the empty grid inside the new window
    outer_frame = tk.Frame(custom_frame, bg="white", bd=2)
    outer_frame.pack(padx=2, pady=2)

    board_inner_frame = tk.Frame(outer_frame, bg="black", bd=2)
    board_inner_frame.pack(padx=1, pady=1)

    boxes = {}
    for br in range(sub_size):
        for bc in range(sub_size):
            box = tk.Frame(board_inner_frame, bg="black", bd=1)
            box.grid(row=br, column=bc, padx=1, pady=1)
            boxes[(br, bc)] = box

    vcmd_custom = (custom_window.register(validate_numeric_input), '%P')

    for r in range(size):
        for c in range(size):
            br, bc = r // sub_size, c // sub_size
            lr, lc = r % sub_size, c % sub_size

            entry = tk.Entry(
                boxes[(br, bc)], 
                width=2, 
                font=("Arial", 11, "bold"), 
                justify="center",
                bg="white",      
                fg="black",      
                insertbackground="black",
                relief="flat",
                validate="key",
                validatecommand=vcmd_custom
            )
            entry.grid(row=lr, column=lc, padx=1, pady=1)
            custom_entries[(r, c)] = entry

    def validate_and_transfer():
        """
        Validates that no two identical numbers exist in the same row or column.
        If valid, copies the custom puzzle into the main window's grid.
        """
        global Timer, Timer_Switch

        board_values = [[0] * size for _ in range(size)]
        
        has_at_least_one = False 
        
        for r in range(size):
            for c in range(size):
                val_str = custom_entries[(r, c)].get().strip()
                if val_str.isdigit() and int(val_str) > 0:
                    board_values[r][c] = int(val_str)
                    has_at_least_one = True
                else:
                    board_values[r][c] = 0

        # The Grid must have at least one number to be valid
        if not has_at_least_one:
            messagebox.showwarning(
                "Tablero Vacío", 
                "Debes ingresar al menos un número en el tablero para poder validarlo y cargarlo.", 
                parent=custom_window
            )
            return
        
        # Read custom values from inputs
        for r in range(size):
            for c in range(size):
                val_str = custom_entries[(r, c)].get().strip()
                if val_str.isdigit():
                    board_values[r][c] = int(val_str)
                else:
                    board_values[r][c] = 0

        # Check row and column constraints for duplicates
        has_duplicates = False

        # 1. Check rows
        for r in range(size):
            seen = set()
            for c in range(size):
                val = board_values[r][c]
                if val != 0:
                    if val in seen:
                        has_duplicates = True
                        break
                    seen.add(val)
            if has_duplicates:
                break

        # 2. Check columns
        if not has_duplicates:
            for c in range(size):
                seen = set()
                for r in range(size):
                    val = board_values[r][c]
                    if val != 0:
                        if val in seen:
                            has_duplicates = True
                            break
                        seen.add(val)
                if has_duplicates:
                    break

        # If duplicate found, show warning and abort transfer
        if has_duplicates:
            messagebox.showwarning(
                "Error de Restricción", 
                "¡Existen números iguales en la misma fila y/o columna! Corrige los valores para continuar.", 
                parent=custom_window
            )
            return
        
        # If valid, copy numbers to the main grid entries and lock them as initial clues
        for r in range(size):
            for c in range(size):
                val = board_values[r][c]
                main_entry = entries.get((r, c))
                if main_entry:
                    main_entry.config(state="normal")
                    main_entry.delete(0, tk.END)
                    if val != 0:
                        main_entry.insert(0, str(val))
                        main_entry.config(state="readonly", readonlybackground="white", fg=ProgramColor)
                    else:
                        main_entry.config(state="normal", bg="white", fg=UserColor)

        messagebox.showinfo("Éxito", "¡Sudoku personalizado cargado e insertado en el tablero principal!", parent=custom_window)
        Timer = 0
        Timer_Switch = True
        Timer_Update()
        custom_window.destroy()

    # 4. Button inside the custom window
    submit_custom_btn = Button(
        custom_window, 
        text="Validar y Cargar al Tablero Principal", 
        command=validate_and_transfer, 
        font=("Arial", 11, "bold"),
        bg="#f0f0f0"
    )
    submit_custom_btn.pack(pady=15)

    def on_close():
        global Timer_Switch, Timer
        Timer_Switch = False
        messagebox.showwarning(
            "Ventana Activa", 
            "Debes completar, validar y cargar tu Sudoku con almenos un numero o usar el botón correspondiente. No puedes cerrar esta ventana directamente.", 
            parent=custom_window
        )

    custom_window.protocol("WM_DELETE_WINDOW", on_close)

def Timer_Update():
    if Timer_Switch:
        global Timer
        Timer += 1

        TimeLabel.config(text=f"Tiempo: {Timer} ms")
        main_window.after(1, Timer_Update)

def RandomBTN_Click():
    set_values(entries)
    global Timer_Switch, Timer, State, Backtracks
    Backtracks = 0
    BacktrackingTextVar.set(f"Retrocesos(Backtracking): {Backtracks}")
    State = 0
    State_Val()
    Timer = 0
    Timer_Switch = True
    Timer_Update()

def CreateBTN_Click():
    global Timer_Switch, Timer, State, Backtracks
    Timer_Switch = False
    Backtracks = 0
    BacktrackingTextVar.set(f"Retrocesos(Backtracking): {Backtracks}")
    State = 0
    State_Val()
    
    open_custom_sudoku_window()
 

def AutoResolveBTN_Click():
    global Timer_Switch, Timer, State, Backtracks
    Backtracks = 0
    BacktrackingTextVar.set(f"Retrocesos(Backtracking): {Backtracks}")
    State = 0
    State_Val()
    Timer = 0
    Timer_Switch = True
    Timer_Update()
    solve_sudoku_from_interface()
    Timer_Switch = False

def SubmitBTN_Click():
    validate_sudoku_solution()
    global Timer_Switch
    WarningMSG = messagebox.askyesno("Warning", "Estas segur@ de proceder?")

    if WarningMSG:
        Timer_Switch = False
    else:
        Timer_Switch = True
        Timer_Update()

# main_window.lift()
# main_window.attributes('-topmost', True)
# main_window.after_idle(main_window.attributes, '-topmost', False)

# UI Elements
title = Label(main_window, text=AppName + " - NxN Generalizado", font=("Currier Newß", 12))
title.pack()

description = Label(main_window, text=AppDescription, font=("Currier Newß", 12))
description.pack()

# Selection Box
SelectionFrame = Frame(main_window)
SelectionFrame.pack(pady=10)

# Dimension Selection
DimensionFrame = Frame(SelectionFrame)
DimensionFrame.pack(side=LEFT)

DimensionVal = ["4x4 (K=2) [Small]", "9x9 (K=3) [Classic]", "16x16 (K=4) [Large]"]
DimensionVar = StringVar()
DimensionVar.set(DimensionVal[0])
DimensionVar.set(list(DimensionVal)[1])  # Set the default value

DimensionLabel = Label(DimensionFrame, text="Dimension:", font=("Currier Newß", 12))
DimensionLabel.pack(side=LEFT)
DimensionEntry = OptionMenu(DimensionFrame, DimensionVar, *DimensionVal, command=SaveSetting)
DimensionEntry.pack(side=LEFT)

# Dificulty Selection
DifficultyFrame = Frame(SelectionFrame)
DifficultyFrame.pack(side=LEFT, padx=10)

DifficultyVal = ["Fácil (45% Vacio)", "Medio (60% Vacio)", "Difícil (75% Vacio)", "Experto (80% Vacio)"]
DifficultyVar = StringVar()
DifficultyVar.set(DifficultyVal[0]) 
DifficultyVar.set(list(DifficultyVal)[0])  # Set the default value

DifficultyLabel = Label(DifficultyFrame, text="Dificultad:", font=("Currier Newß", 12))
DifficultyLabel.pack(side=LEFT)
DifficultyEntry = OptionMenu(DifficultyFrame, DifficultyVar, *DifficultyVal)
DifficultyEntry.pack(side=LEFT)

# Algorithm Selection
AlgorithmFrame = Frame(SelectionFrame)
AlgorithmFrame.pack(side=LEFT)

AlgorithmVal = ["Nivel 1: Básico (DFS)", "Nivel 2: MRV Clásico", "Nivel 3: MRV + Bitmasks O(1)"]
AlgorithmVar = StringVar()
AlgorithmVar.set(AlgorithmVal[0])
AlgorithmVar.set(list(AlgorithmVal)[0])  # Set the default value

AlgorithmLabel = Label(AlgorithmFrame, text="Algoritmo:", font=("Currier Newß", 12))
AlgorithmLabel.pack(side=LEFT)
AlgorithmEntry = OptionMenu(AlgorithmFrame, AlgorithmVar, *AlgorithmVal)
AlgorithmEntry.pack(side=LEFT)

DimensionVar.trace_add("write", lambda *args: SaveSetting())
DifficultyVar.trace_add("write", lambda *args: SaveSetting())
AlgorithmVar.trace_add("write", lambda *args: SaveSetting())

SaveSetting()
State_Val()

# Buttons Frame
ButtonsFrame = Frame(main_window)
ButtonsFrame.pack()

RandomGenBTN = Button(ButtonsFrame, command=RandomBTN_Click, text="Generar Sudoku Aleatorio", font=("Currier Newß", 12))
RandomGenBTN.pack(side=LEFT)

CreateBTN = Button(ButtonsFrame, command=CreateBTN_Click, text="Crear mi propio Sudoku", font=("Currier Newß", 12))
CreateBTN.pack(side=LEFT, padx=10)

ResolveBTN = Button(ButtonsFrame, command=AutoResolveBTN_Click, text="Resolver Sudoku Ahora", font=("Currier Newß", 12))
ResolveBTN.pack(side=LEFT)

# Sudoku Board Frame
BoardFrame = Frame(main_window)
BoardFrame.pack(pady=10)
DrawGrid(BoardFrame, GridSizeVar.get())

SendButtomFrame = Frame(main_window)
SendButtomFrame.pack(side=TOP)

SendButton = Button(SendButtomFrame, text="Submit", command=SubmitBTN_Click, font=("Currier Newß", 12))
SendButton.pack(side=TOP)

# Fotter Frame
FotterFrame = Frame(main_window)
FotterFrame.pack(side=BOTTOM)

# Left Fotter Frame
LeftFotterFrame = Frame(FotterFrame)
LeftFotterFrame.pack(side=LEFT, pady=15)

FotterTitleLabel = Label(LeftFotterFrame, text="Telemetria de Complejidad y Rendimiento", font=("Currier Newß", 12))
FotterTitleLabel.pack(side=TOP)

SubFrame0 = Frame(LeftFotterFrame)
SubFrame0.pack(side=TOP)

StateFrame = Frame(SubFrame0)
StateFrame.pack(side=LEFT)

StateLabel = Label(StateFrame, textvariable=StateTextVar, font=("Currier Newß", 12))
StateLabel.pack()

SubFrame = Frame(LeftFotterFrame)
SubFrame.pack(side=TOP)

TimeFrame = Frame(SubFrame)
TimeFrame.pack(side=LEFT, padx=20)

TimeLabel = Label(TimeFrame, text="Tiempo: " + str(Timer) + " ms", font=("Currier Newß", 12))
TimeLabel.pack()

BacktrackingFrame = Frame(SubFrame)
BacktrackingFrame.pack(side=RIGHT)

BacktrackingTextVar.set(f"Retrocesos(Backtracking): {Backtracks}")
BacktrackingLabel = Label(BacktrackingFrame, textvariable=BacktrackingTextVar, font=("Currier Newß", 12))
BacktrackingLabel.pack()

#Right Fotter Frame
RightFotterFrame = Frame(FotterFrame)
RightFotterFrame.pack(side=LEFT, padx=30)

GridLabel = Label(RightFotterFrame, textvariable=GridTextVar, font=("Currier Newß", 12))
GridLabel.pack(side=BOTTOM)

# Start the main Window
main_window.mainloop()