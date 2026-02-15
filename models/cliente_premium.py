from models.cliente import Cliente


class ClientePremium(Cliente):
    def calcular_descuento(self, monto: float) -> float:
        return monto * 0.10  # 10% descuento
