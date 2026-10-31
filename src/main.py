from tkinter import *
from tkinter import messagebox
import tkinter as tk

# App Info
AppName = "Sudoku Studio"
AppDescription = "NxN Sudoku Puzzle Generator and Solver. Motor de Heuristica con Backtracking y Poda (CSP) - CC184"
version = "1.0.0"

# Main Window
main_window = Tk()
main_window.title(AppName + " v" + version)
main_window.geometry("1000x1000")

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

BoardFrame  = None

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
    else:
        State = 0
        StateVal["Solved"] = "no resuelto"
        
    StateTextVar.set(f"Estado: Sudoku {GridSizeVar.get()} {StateVal['Solved']}")

def DrawGrid_in_Frame(Frame_Container, size):
    for widget in Frame_Container.winfo_children():
        widget.destroy()

    sub_size = int(size**0.5)
    entries = {}

    if size == 16:
        font_size = 9      
        entry_width = 2    
        pad_space = 0      
    elif size == 9:
        font_size = 11
        entry_width = 2
        pad_space = 1
    else: 
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
                relief="flat"
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

def Timer_Update():
    if Timer_Switch:
        global Timer
        Timer += 1

        TimeLabel.config(text=f"Tiempo: {Timer} ms")
        main_window.after(1, Timer_Update)

def RandomBTN_Click():
    global Timer_Switch, Timer
    Timer = 0
    Timer_Switch = True
    Timer_Update()

def CreateBTN_Click():
    pass

def AutoResolveBTN_Click():
    global Timer_Switch, Timer
    Timer = 0
    Timer_Switch = True
    Timer_Update()
    # Procediment
    Timer_Switch = False

def SubmitBTN_Click():
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

SendButton = Button(SendButtomFrame, command=SubmitBTN_Click, text="Submit", font=("Currier Newß", 12))
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

BacktrackingLabel = Label(BacktrackingFrame, text="Retrocesos(Backtracking): " + str(Backtracks), font=("Currier Newß", 12))
BacktrackingLabel.pack()

#Right Fotter Frame
RightFotterFrame = Frame(FotterFrame)
RightFotterFrame.pack(side=LEFT, padx=30)

GridLabel = Label(RightFotterFrame, textvariable=GridTextVar, font=("Currier Newß", 12))
GridLabel.pack(side=BOTTOM)

# Start the main Window
main_window.mainloop()