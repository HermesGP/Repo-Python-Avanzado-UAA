def test_crear_grafo_3_por_3():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(3)
    assert grafo.cantidad_vertices == 3
    assert grafo.matriz == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

def test_agregar_arista():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(3)
    grafo.agregar_arista(0, 1)
    assert grafo.matriz == [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

def test_eliminar_arista():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(3)
    grafo.agregar_arista(0, 1)
    grafo.eliminar_arista(0, 1)
    assert grafo.matriz == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

def test_dfs():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(3)
    grafo.agregar_arista(0, 1)
    grafo.agregar_arista(1, 2)
    assert grafo.dfs(0) == [0, 1, 2]

def test_eliminar_vertice():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(3)
    grafo.agregar_arista(0, 1)
    grafo.agregar_arista(1, 2)
    grafo.eliminar_vertice(1)
    assert grafo.cantidad_vertices == 2
    assert grafo.matriz == [
        [0, 0],
        [0, 0]
    ]

def test_agregar_vertice():
    from grafo.grafo_matriz_adyacencia import Grafo
    grafo = Grafo(2)
    grafo.agregar_vertice()
    assert grafo.cantidad_vertices == 3
    assert grafo.matriz == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]