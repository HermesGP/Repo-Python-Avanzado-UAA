#Crear una clase para imprimir un índice, usando context manager anidados
class Indice:
    def __init__(self):
        self.nivel = []
        self.lineas = []
    def __enter__(self):
        #Aumentar el nivel del índice y agregar una línea al índice con el número de nivel y el título del ítem
        self.nivel.append(0)
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        #Disminuir el nivel del índice y eliminar la última línea del índice
        self.nivel.pop()
        return False
    def seccion(self, titulo):
        return Seccion(self, titulo)
    def item(self, titulo):
        #Aumentar el nivel del último elemento de la lista de niveles y agregar una línea al índice con el número de nivel y el título del ítem
        self.nivel[-1] += 1
        self.lineas.append(f"{'.'.join([str(n) for n in self.nivel])} {titulo}")
    def imprimir(self):
        for linea in self.lineas:
            print(linea)

class Seccion:
    def __init__(self, indice, titulo):
        self.indice = indice
        self.titulo = titulo
    def __enter__(self):
        #Aumentar el nivel del índice y agregar una línea al índice con el número de nivel y el título de la sección
        self.indice.nivel[-1] += 1
        self.indice.lineas.append(f"{'.'.join([str(n) for n in self.indice.nivel])} {self.titulo}")
        self.indice.nivel.append(0)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #Disminuir el nivel del índice y eliminar la última línea del índice
        self.indice.nivel.pop()
        return False
if __name__ == "__main__":
    with Indice() as indice:
        with indice.seccion("Sistemas Operativos"):
            indice.item("Windows")
            indice.item("MacOS")
            with indice.seccion("Distribuciones Linux"):
                indice.item("Debian y derivados")
                indice.item("Arch y derivados")
        with indice.seccion("Lenguajes de programación"):
            indice.item("Definicion")
            with indice.seccion("Lenguajes compilados"):
                indice.item("C y C++")
            with indice.seccion("Lenguajes interpretados"):
                indice.item("Python")
                indice.item("JavaScript")
    indice.imprimir()