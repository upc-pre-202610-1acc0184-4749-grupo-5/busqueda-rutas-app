from tkinter import *

# App Info
AppName = "Sudoku Studio"
AppDescription = "NxN Sudoku Puzzle Generator and Solver. Motor de Heuristica con Backtracking y Poda (CSP) - CC184"
version = "1.0.0"

# Main Window
main_window = Tk()
main_window.title(AppName + " v" + version)
main_window.geometry("1000x1000")

x = 0

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

Dimension = ["4x4 (K=2) [Small]", "9x9 (K=3) [Classic]", "16x16 (K=4) [Large]"]
DimensionVar = StringVar()
DimensionVar.set(list(Dimension)[1])  # Set the default value

DimensionLabel = Label(DimensionFrame, text="Dimension:", font=("Currier Newß", 12))
DimensionLabel.pack(side=LEFT)
DimensionEntry = OptionMenu(DimensionFrame, DimensionVar, *Dimension)
DimensionEntry.pack(side=LEFT)

# Dificulty Selection
DificultyFrame = Frame(SelectionFrame)
DificultyFrame.pack(side=LEFT, padx=10)

Dificulty = ["Fácil (45% Vacio)", "Medio (60% Vacio)", "Difícil (75% Vacio)", "Experto (80% Vacio)"]
DificultyVar = StringVar()
DificultyVar.set(list(Dificulty)[0])  # Set the default value

DificultyLabel = Label(DificultyFrame, text="Dificultad:", font=("Currier Newß", 12))
DificultyLabel.pack(side=LEFT)
DificultyEntry = OptionMenu(DificultyFrame, DificultyVar, *Dificulty)
DificultyEntry.pack(side=LEFT)

# Algorithm Selection
AlgorithmFrame = Frame(SelectionFrame)
AlgorithmFrame.pack(side=LEFT)

Algorithm = ["Nivel 1: Básico (DFS)", "Nivel 2: MRV Clásico", "Nivel 3: MRV + Bitmasks O(1)"]
AlgorithmVar = StringVar()
AlgorithmVar.set(list(Algorithm)[0])  # Set the default value

AlgorithmLabel = Label(AlgorithmFrame, text="Algoritmo:", font=("Currier Newß", 12))
AlgorithmLabel.pack(side=LEFT)
AlgorithmEntry = OptionMenu(AlgorithmFrame, AlgorithmVar, *Algorithm)
AlgorithmEntry.pack(side=LEFT)

# Buttons Frame
ButtonsFrame = Frame(main_window)
ButtonsFrame.pack()

RandomGenBTN = Button(ButtonsFrame, text="Generar Sudoku Aleatorio", font=("Currier Newß", 12))
RandomGenBTN.pack(side=LEFT)

CreateBTN = Button(ButtonsFrame, text="Crear mi propio Sudoku", font=("Currier Newß", 12))
CreateBTN.pack(side=LEFT, padx=10)

ResolveBTN = Button(ButtonsFrame, text="Resolver Sudoku Ahora", font=("Currier Newß", 12))
ResolveBTN.pack(side=LEFT)

# Sudoku Board Frame
BoardFrame = Frame(main_window)
BoardFrame.pack(pady=10)

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

StateLabel = Label(StateFrame, text="Estado: ", font=("Currier Newß", 12))
StateLabel.pack()

SubFrame = Frame(LeftFotterFrame)
SubFrame.pack(side=TOP)

TimeFrame = Frame(SubFrame)
TimeFrame.pack(side=LEFT, padx=20)

TimeLabel = Label(TimeFrame, text="Tiempo: " + str(x) + " ms", font=("Currier Newß", 12))
TimeLabel.pack()

BacktrackingFrame = Frame(SubFrame)
BacktrackingFrame.pack(side=RIGHT)

BacktrackingLabel = Label(BacktrackingFrame, text="Retrocesos(Backtracking): ", font=("Currier Newß", 12))
BacktrackingLabel.pack()

#Right Fotter Frame
RightFotterFrame = Frame(FotterFrame)
RightFotterFrame.pack(side=LEFT, padx=30)

GridLabel = Label(RightFotterFrame, text="Cuadricula: ", font=("Currier Newß", 12))
GridLabel.pack(side=BOTTOM)

# Start the main Window
main_window.mainloop()