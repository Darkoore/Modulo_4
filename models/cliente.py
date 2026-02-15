class Cliente:
    def __init__(self, rut: str, nombre: str, correo: str):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo

    def calcular_descuento(self, monto: float) -> float:
        """
        Método base que será sobrescrito por las subclases.
        """
        return 0

    def mostrar_datos(self):
        print(f"Cliente: {self.nombre} | RUT: {self.rut} | Correo: {self.correo}")
