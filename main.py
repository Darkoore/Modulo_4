from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_ejecutivo import ClienteEjecutivo


clientes = [
    ClienteRegular("12345678-9", "Ignacio", "ignacio@mail.com"),
    ClientePremium("98765432-1", "Maria", "maria@mail.com"),
    ClienteEjecutivo("11222333-4", "Carlos", "carlos@mail.com")
]

monto_compra = 100000

for cliente in clientes:
    cliente.mostrar_datos()
    descuento = cliente.calcular_descuento(monto_compra)
    print(f"Descuento aplicado: ${descuento}")
    print("-" * 40)
