from models.cliente import Cliente


class ClienteEjecutivo(Cliente):
    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.20  # 20% descuento
