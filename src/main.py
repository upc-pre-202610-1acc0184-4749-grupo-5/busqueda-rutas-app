from tkinter import *

# App Info
AppName = "Busqueda Rutas App"
AppDescription = " "
version = "1.0.0"

window = Tk()
window.title(AppName + " v" + version)
window.geometry("500x500")

window.lift()
window.attributes('-topmost', True)
window.after_idle(window.attributes, '-topmost', False)

window.mainloop()