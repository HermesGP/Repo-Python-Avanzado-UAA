from arbol.arbol_binario import ArbolBinario

import pytest

@pytest.fixture
def arbol():
    return ArbolBinario()

def test_agregar_y_enorden(arbol):
    arbol.agregar(10)
    arbol.agregar(5)
    arbol.agregar(15)
    assert arbol.enorden() == [5, 10, 15]

def test_agregar_valores_duplicados(arbol):
    arbol.agregar(10)
    arbol.agregar(5)
    arbol.agregar(15)
    arbol.agregar(10)
    assert arbol.enorden() == [5, 10, 10, 15]

def test_arbol_vacio(arbol):
    assert arbol.enorden() == []