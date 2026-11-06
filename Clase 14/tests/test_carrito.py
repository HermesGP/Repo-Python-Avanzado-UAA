import pytest
from tienda.carrito import Carrito
from tienda.modelo import Producto
from tienda.precios import calcular_total

@pytest.fixture
def producto():
    return Producto(nombre="Teclado Mecánico Ajazz", precio=350000)
@pytest.fixture
def producto2():
    return Producto(nombre="Mouse Gamer Logitech", precio=150000)
@pytest.fixture
def carrito():
    return Carrito()

def test_carrito(carrito, producto, producto2):
    assert carrito.cantidad_total() == 0
    assert carrito.subtotal() == 0
    carrito.agregar(producto, cantidad=2)
    carrito.agregar(producto2, cantidad=1)
    assert carrito.cantidad_total() == 3
    assert carrito.subtotal() == 850000
    carrito.vaciar()
    assert carrito.cantidad_total() == 0
    assert carrito.subtotal() == 0

def test_carrito_cantidad_invalida(carrito, producto):
    with pytest.raises(ValueError) as e:
        carrito.agregar(producto, cantidad=0)
    assert str(e.value) == "La cantidad debe ser mayor que cero"

def test_carrito_producto_inactivo(carrito):
    producto = Producto(nombre="Teclado Mecánico Razer", precio=1550000, activo=False)
    with pytest.raises(ValueError) as e:
        carrito.agregar(producto, cantidad=1)
    assert str(e.value) == "El producto no está activo"

def test_carrito_vacio(carrito):
    assert carrito.items == []

def test_carrito_total(carrito, producto):
    carrito.agregar(producto, cantidad=2)
    assert carrito.subtotal() == 700000
    assert calcular_total(carrito.subtotal(), descuento=20.0, impuesto=10.0) == 616000

@pytest.mark.parametrize("cantidad, mensaje", [
    (0, "La cantidad debe ser mayor que cero"),
    (-1, "La cantidad debe ser mayor que cero")
])
def test_carrito_errores_param(carrito, producto, cantidad, mensaje):
    with pytest.raises(ValueError) as e:
        carrito.agregar(producto, cantidad=cantidad)
    assert str(e.value) == mensaje