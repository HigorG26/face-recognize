import tkinter as tk
from frame import InterfaceGrafica
from service import ProcessadorImagens

def main():
    root = tk.Tk()
    processador = ProcessadorImagens()
    app = InterfaceGrafica(root, processador)
    root.mainloop()

if __name__ == "__main__":
    main()
