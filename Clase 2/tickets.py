from collections import deque

def main():
    colaTickets = deque()

    print("Insertando 3 tickets en la cola: A01, B02, C03")
    colaTickets.append("A01")
    colaTickets.append("B02")
    colaTickets.append("C03")

    print(f"Cantidad de elementos de la cola: {len(colaTickets)}")
    print(f"Elemento que está primero: {colaTickets[0]}")

    for ticket in colaTickets:
        print(ticket)

    print(f"Extraemos un elemento de la cola: {colaTickets.popleft()}")
    print(f"Cantidad de elementos de la cola: {len(colaTickets)}")

    for ticket in colaTickets:
        print(ticket)


if __name__ == "__main__":
    main()
