import tkinter as tk


class MenuFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        tk.Label(self, text="MENÚ PRINCIPAL", font=("Arial", 18)).pack(pady=30)

        tk.Button(self,text="Compras",
                  width=25,height=2,command=lambda: controller.show_frame("ComprasFrame")).pack(pady=10)
        
        tk.Button(self,text="Gestión Clientes",
                  width=25,height=2,command=lambda: controller.show_frame("GestionClientesFrame")).pack(pady=10)

        tk.Button(self,text="Salir",
                  width=25,height=2,command=controller.root.quit).pack(pady=10)