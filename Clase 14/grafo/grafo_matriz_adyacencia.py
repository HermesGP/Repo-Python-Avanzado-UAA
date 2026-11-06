class Grafo:
    def __init__(self, cantidad_vertices: int):
        self.cantidad_vertices = cantidad_vertices

        # Inicializa una matriz de NxN con ceros
        self.matriz = [
            [0 for _ in range(cantidad_vertices)]
            for _ in range(cantidad_vertices)
        ]

    def agregar_arista(self, origen: int, destino: int):
        self.matriz[origen][destino] = 1

    def eliminar_arista(self, origen: int, destino: int):
        self.matriz[origen][destino] = 0

    def existe_arista(self, origen: int, destino: int) -> bool:
        return self.matriz[origen][destino] == 1

    def mostrar(self):
        print("Matriz de adyacencia:")
        for fila in self.matriz:
            print(fila)

    def dfs(self, inicio: int):
        visitado = [False] * self.cantidad_vertices
        resultado = []

        def dfs_recursivo(v):
            visitado[v] = True
            resultado.append(v)
            for i in range(self.cantidad_vertices):
                if self.matriz[v][i] == 1 and not visitado[i]:
                    dfs_recursivo(i)

        dfs_recursivo(inicio)
        return resultado
    
    def eliminar_vertice(self, vertice: int):
        # Elimina todas las aristas asociadas al vértice
        for i in range(self.cantidad_vertices):
            self.matriz[vertice][i] = 0
            self.matriz[i][vertice] = 0
        # Elimina la fila y columna correspondiente al vértice
        self.matriz.pop(vertice)
        for fila in self.matriz:
            fila.pop(vertice)
        self.cantidad_vertices -= 1
    
    def agregar_vertice(self):
        self.cantidad_vertices += 1
        for fila in self.matriz:
            fila.append(0)
        self.matriz.append([0 for _ in range(self.cantidad_vertices)])