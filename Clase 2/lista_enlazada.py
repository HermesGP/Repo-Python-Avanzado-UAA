class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.next = None

    def __str__(self):
        return str(self.valor)


class ListaEnlazada:
    def __init__(self):
        self.head = None

    def esta_vacia(self):
        return self.head is None

    def insertar_inicio(self, valor):
        nuevo = Nodo(valor)
        nuevo.next = self.head
        self.head = nuevo

    def insertar_final(self, valor):
        nuevo = Nodo(valor)
        if self.esta_vacia():
            self.head = nuevo
            return

        actual = self.head
        while actual.next:
            actual = actual.next
        actual.next = nuevo

    def buscar(self, valor):
        actual = self.head
        while actual:
            if actual.valor == valor:
                return True
            actual = actual.next
        return False

    def eliminar(self, valor):
        if self.esta_vacia():
            return

        actual = self.head
        previo = None

        while actual and actual.valor != valor:
            previo = actual
            actual = actual.next

        if not actual:
            return  # no encontrado

        if previo is None:
            self.head = actual.next  # eliminar el primero
        else:
            previo.next = actual.next

    def recorrer(self):
        actual = self.head
        while actual:
            print(actual.valor)
            actual = actual.next