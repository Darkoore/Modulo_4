# models/cliente_regular.py

from models.cliente import Cliente


class ClienteRegular(Cliente):
    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.05  # 5% descuento
