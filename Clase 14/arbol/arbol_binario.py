class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None
    def agregar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._agregar_recursivo(self.raiz, valor)

    def _agregar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._agregar_recursivo(nodo.izquierda, valor)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._agregar_recursivo(nodo.derecha, valor)
    def enorden(self):
        return self._enorden_recursivo(self.raiz)

    def _enorden_recursivo(self, nodo):
        if nodo is None:
            return []
        return self._enorden_recursivo(nodo.izquierda) + [nodo.valor] + self._enorden_recursivo(nodo.derecha)

    def preorden(self):
        return self._preorden_recursivo(self.raiz)

    def _preorden_recursivo(self, nodo):
        if nodo is None:
            return []
        return [nodo.valor] + self._preorden_recursivo(nodo.izquierda) + self._preorden_recursivo(nodo.derecha)

    def postorden(self):
        return self._postorden_recursivo(self.raiz)

    def _postorden_recursivo(self, nodo):
        if nodo is None:
            return []
        return self._postorden_recursivo(nodo.izquierda) + self._postorden_recursivo(nodo.derecha) + [nodo.valor]
    