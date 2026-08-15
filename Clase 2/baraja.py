import random

Palos = ("Oros", "Copas", "Espadas", "Bastos")

class Carta:
    def __init__(self, palo, numero):
        self.palo = palo
        self.numero = numero

    def __str__(self):
        return f"{self.numero} de {self.palo}"

class BarajaEspañola:
    def __init__(self):
        self.cartas = [Carta(palo, numero) for palo in Palos for numero in range(1, 13) if numero != 8 and numero != 9]

    def barajar(self):
        random.shuffle(self.cartas)

    def robar_cartas(self, cantidad):
        mano = []
        if cantidad <= 0:
            print("La cantidad de cartas a robar debe ser mayor que cero.")
            return None
        for _ in range(cantidad):
            if self.cartas:
                mano.append(self.cartas.pop())
            else:
                print("No hay más cartas en la baraja.")
                break
        return mano if mano else None

    def devolver_cartas(self, carta):
 
        if not carta:
            print("No se puede devolver una carta nula.")
            return
        if carta in self.cartas:
            print("La carta ya está en la baraja.")
            return
        self.cartas.append(carta)
        self.barajar()

if __name__ == "__main__":
    baraja = BarajaEspañola()
    baraja.barajar()

    print("Robando 5 cartas:")
    mano = baraja.robar_cartas(5)
    if mano:
        for carta in mano:
            print(carta)

    print("\nDevolviendo una carta a la baraja:")
    if mano:
        primera_carta = mano.pop(0)
        baraja.devolver_cartas(primera_carta)
        print(f"Se devolvió: {primera_carta}")

    print("\nDevolviendo mi mano al mazo:")
    if mano:
        for carta in mano:
            baraja.devolver_cartas(carta)
            print(f"Se devolvió: {carta}")