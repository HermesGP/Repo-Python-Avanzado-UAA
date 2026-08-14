import random

PALOS = {"Oros", "Copas", "Espadas", "Bastos"}

class Carta:
    def __init__(self, palo, numero):
        self.palo = palo
        self.numero = numero

    def __str__(self):
        return f"{self.numero} de {self.palo}"

class BarajaEspanola:
    def __init__(self):
        self.cartas = []
        self._iniciar_baraja()
        self._mezclar()

    def _iniciar_baraja(self):
        for palo in PALOS:
            for numero in range(1, 13):
                if numero not in (8, 9):  # excluir 8 y 9
                    self.cartas.append(Carta(palo, numero))

    def _mezclar(self):
        random.shuffle(self.cartas)

    def sacar_cartas(self, cantidad):
        if cantidad <= 0:
            print("El número de cartas debe ser mayor a cero.")
            return None

        if not self.cartas:
            print("La baraja está vacía.")
            return None

        mano = []
        for _ in range(cantidad):
            if self.cartas:
                mano.append(self.cartas.pop())
            else:
                print("No quedan más cartas.")
                break

        return mano

    def devolver_carta(self, carta):
        if carta is None:
            print("No se puede devolver una carta nula.")
            return

        if carta in self.cartas:
            print("La carta ya está en la baraja.")
            return

        self.cartas.append(carta)
        print(f"Carta devuelta: {carta}")
        self._mezclar()


def main():
    baraja = BarajaEspanola()

    mano = baraja.sacar_cartas(3)
    print("Mi mano es:")
    for carta in mano:
        print(carta)

    print("Devolviendo mi mano al mazo...")
    for carta in mano:
        baraja.devolver_carta(carta)

    mano = baraja.sacar_cartas(3)
    print("Mi nueva mano es:")
    for carta in mano:
        print(carta)

    print("Devolviendo mi nueva mano al mazo...")
    for carta in mano:
        baraja.devolver_carta(carta)

    print("Intentando devolver nuevamente las mismas cartas...")
    for carta in mano:
        baraja.devolver_carta(carta)


if __name__ == "__main__":
    main()