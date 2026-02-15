import sqlite3
from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_ejecutivo import ClienteEjecutivo


class DatabaseManager:

    def __init__(self, db_name="clientes.db"):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
        """)

        conexion.commit()
        conexion.close()

    def guardar_cliente(self, cliente):
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
            INSERT INTO clientes (rut, nombre, correo, tipo)
            VALUES (?, ?, ?, ?)
            """, (cliente.rut, cliente.nombre, cliente.correo, type(cliente).__name__))

            conexion.commit()

        except sqlite3.IntegrityError:
            print("Error: Ya existe un cliente con ese RUT.")

        finally:
            conexion.close()

    def obtener_clientes(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT rut, nombre, correo, tipo FROM clientes")
        filas = cursor.fetchall()

        conexion.close()

        clientes = []

        for rut, nombre, correo, tipo in filas:
            if tipo == "ClienteRegular":
                clientes.append(ClienteRegular(rut, nombre, correo))
            elif tipo == "ClientePremium":
                clientes.append(ClientePremium(rut, nombre, correo))
            elif tipo == "ClienteEjecutivo":
                clientes.append(ClienteEjecutivo(rut, nombre, correo))

        return clientes
    def existe_rut(self, rut):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT 1 FROM clientes WHERE rut = ?", (rut,))
        resultado = cursor.fetchone()

        conexion.close()

        return resultado is not None
    def eliminar_cliente(self, rut):
        conexion = self.conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM clientes WHERE rut = ?", (rut,))

        conexion.commit()
        filas_afectadas = cursor.rowcount
        conexion.close()
        return filas_afectadas
