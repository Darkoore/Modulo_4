import tkinter as tk
from tkinter import ttk, messagebox

from database.db_manager import DatabaseManager
from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_ejecutivo import ClienteEjecutivo


class GestionClientesFrame(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.db = DatabaseManager()

        self.crear_widgets()

    def crear_widgets(self):

        # Título
        tk.Label(self, text="Gestión de Clientes", font=("Arial", 16))\
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Labels
        tk.Label(self, text="RUT").grid(row=1, column=0)
        tk.Label(self, text="Nombre").grid(row=2, column=0)
        tk.Label(self, text="Correo").grid(row=3, column=0)
        tk.Label(self, text="Tipo Cliente").grid(row=4, column=0)

        # Entradas
        self.entry_rut = tk.Entry(self, justify="center")
        self.entry_nombre = tk.Entry(self, justify="center")
        self.entry_correo = tk.Entry(self, justify="center")

        self.entry_rut.grid(row=1, column=1, padx=10, pady=5)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=5)
        self.entry_correo.grid(row=3, column=1, padx=10, pady=5)

        # Combobox tipo cliente
        self.tipo_cliente = ttk.Combobox(self, state='readonly')
        self.tipo_cliente["values"] = ("Regular", "Premium", "Ejecutivo")
        self.tipo_cliente.grid(row=4, column=1)
        self.tipo_cliente.current(0)

        # Botones
        tk.Button(self, text="Guardar", command=self.guardar_cliente)\
            .grid(row=5, column=0, columnspan=2)

        tk.Button(self, text="Eliminar Seleccionado", command=self.eliminar_cliente)\
            .grid(row=6, column=0, columnspan=2)

        tk.Button(
            self,
            text="Volver al Menú",
            command=lambda: self.controller.show_frame("MenuFrame")
        ).grid(row=7, column=0, columnspan=2, pady=10)

        # Lista clientes
        self.lista_clientes = tk.Listbox(self, width=100, height=10)
        self.lista_clientes.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

        self.cargar_clientes()

    def guardar_cliente(self):

        rut = self.entry_rut.get()
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        tipo = self.tipo_cliente.get()
        #Validaciones previo ingreso
        
        if not rut or not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if self.db.existe_rut(rut):
            messagebox.showerror("Error", "El RUT ya está registrado")
            return

        # Validación RUT
        if len(rut) != 10:
            messagebox.showerror("Error", "El RUT debe tener formato 12345678-9")
            return

        if rut[8] != "-":
            messagebox.showerror("Error", "Por favor añadir '-' en el RUT")
            return

        parte_numerica = rut[:8]
        digito_verificador = rut[9]

        if not parte_numerica.isdigit():
            messagebox.showerror("Error", "Los primeros 8 caracteres deben ser números")
            return

        if not digito_verificador.isalnum():
            messagebox.showerror("Error", "Dígito verificador no válido")
            return

        if "@" not in correo:
            messagebox.showerror("Error", "El correo debe contener @")
            return False
        
        if correo.count("@") != 1:
            messagebox.showerror("Error", "El correo debe contener solo un @")
            return False
        
        # Crear cliente según tipo
        if tipo == "Regular":
            cliente = ClienteRegular(rut, nombre, correo)
        elif tipo == "Premium":
            cliente = ClientePremium(rut, nombre, correo)
        else:
            cliente = ClienteEjecutivo(rut, nombre, correo)

        self.db.guardar_cliente(cliente)

        messagebox.showinfo("Éxito", "Cliente guardado correctamente")

        self.limpiar_campos()
        self.cargar_clientes()

    def cargar_clientes(self):

        self.lista_clientes.delete(0, tk.END)

        clientes = self.db.obtener_clientes()

        for cliente in clientes:
            self.lista_clientes.insert(
                tk.END,
                f"RUT: {cliente.rut} | Nombre: {cliente.nombre} | Correo: {cliente.correo} | Tipo: {type(cliente).__name__}"
            )

    def limpiar_campos(self):

        self.entry_rut.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

    def eliminar_cliente(self):

        seleccion = self.lista_clientes.curselection()

        if not seleccion:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
            return

        texto = self.lista_clientes.get(seleccion[0])
        rut = texto.split(" | ")[0].replace("RUT: ", "")

        filas = self.db.eliminar_cliente(rut)

        if filas == 0:
            messagebox.showerror("Error", "No se pudo eliminar el cliente")
        else:
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.cargar_clientes()
