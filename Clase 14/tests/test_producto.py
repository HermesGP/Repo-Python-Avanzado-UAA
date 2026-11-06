
import pytest
from tienda.modelo import Producto
def test_producto():
    producto = Producto(nombre="Teclado Mecánico Ajazz", precio=350000)
    assert producto.nombre == "Teclado Mecánico Ajazz"
    assert producto.precio == 350000
    assert producto.activo is True

def test_producto_inactivo():
    producto = Producto(nombre="Teclado Mecánico Ajazz", precio=350000, activo=False)
    assert producto.activo is False

@pytest.mark.parametrize("nombre, precio, activo", [
    ("Teclado Mecánico Ajazz", 350000, True),
    ("Teclado Mecánico Razer", 1550000, False)
])
def test_producto_param(nombre, precio, activo):
    producto = Producto(nombre=nombre, precio=precio, activo=activo)
    assert producto.nombre == nombre
    assert producto.precio == precio
    assert producto.activo is activo
    
def test_producto_nombre_vacio():
    with pytest.raises(ValueError) as e:
        Producto(nombre="", precio=350000)
    assert str(e.value) == "El nombre del producto es obligatorio"

def test_producto_precio_invalido():
    with pytest.raises(ValueError) as e:
        Producto(nombre="Teclado Mecánico Ajazz", precio=0)
    assert str(e.value) == "El precio debe ser mayor que cero"