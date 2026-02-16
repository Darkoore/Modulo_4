import tkinter as tk
from tkinter import ttk, messagebox

from database.db_manager import DatabaseManager


class ComprasFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.db = DatabaseManager()

        self.crear_widgets()
    
    
    def on_show(self):
      self.cargar_clientes()

    def crear_widgets(self):
        #Centrado de pagina
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="MÓDULO DE COMPRAS", font=("Arial", 16))\
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Cliente
        tk.Label(self, text="Seleccionar Cliente").grid(row=1, column=0)

        self.combo_clientes = ttk.Combobox(self, state="readonly", width=40)
        self.combo_clientes.grid(row=1, column=1, pady=5)

        # Monto
        tk.Label(self, text="Monto Compra").grid(row=2, column=0)

        self.entry_monto = tk.Entry(self, width=40)
        self.entry_monto.grid(row=2, column=1, pady=5)

        # Validar solo números
        self.entry_monto.bind("<KeyRelease>", self.validar_numeros)

        # Botón calcular
        tk.Button(
            self,
            text="Calcular Descuento",
            command=self.calcular_descuento
        ).grid(row=3, column=0, columnspan=2, pady=10)

        # Volver
        tk.Button(
            self,
            text="Volver al Menú",
            command=lambda: self.controller.show_frame("MenuFrame")
        ).grid(row=4, column=0, columnspan=2, pady=10)

        self.cargar_clientes()

    def cargar_clientes(self):

        clientes = self.db.obtener_clientes()

        self.clientes_dict = {}

        lista = []

        for cliente in clientes:
            texto = f"{cliente.nombre} ({cliente.rut})"
            lista.append(texto)
            self.clientes_dict[texto] = cliente

        self.combo_clientes["values"] = lista

        if lista:
            self.combo_clientes.current(0)
        else:
            self.combo_clientes.set("")

    def validar_numeros(self, event):

        valor = self.entry_monto.get()

        if not valor.isdigit():
            self.entry_monto.delete(0, tk.END)
            self.entry_monto.insert(0, ''.join(filter(str.isdigit, valor)))

    def calcular_descuento(self):

        cliente_seleccionado = self.combo_clientes.get()
        monto_texto = self.entry_monto.get()

        if not cliente_seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente")
            return

        if not monto_texto:
            messagebox.showerror("Error", "Ingrese un monto válido")
            return

        cliente = self.clientes_dict[cliente_seleccionado]
        monto = float(monto_texto)

        descuento = cliente.calcular_descuento(monto)
        total = monto - descuento

        self.mostrar_resultado(monto, descuento, total)

    def mostrar_resultado(self, monto, descuento, total):

        ventana = tk.Toplevel(self)
        ventana.title("Resultado Compra")

        tk.Label(ventana, text=f"Monto original: ${monto:.2f}")\
            .pack(pady=5)

        tk.Label(ventana, text=f"Descuento aplicado: ${descuento:.2f}")\
            .pack(pady=5)

        tk.Label(ventana, text=f"Total a pagar: ${total:.2f}", font=("Arial", 12, "bold"))\
            .pack(pady=10)
