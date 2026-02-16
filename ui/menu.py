import tkinter as tk

class MenuFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Menú Principal").pack(pady=20)

        tk.Button(self, text="Compra",
                  command=controller.mostrar_compras).pack(pady=5)

        tk.Button(self, text="Gestión de Clientes",
                  command=controller.mostrar_gestion).pack(pady=5)
