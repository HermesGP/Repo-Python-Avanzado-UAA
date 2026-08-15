from collections import deque

if __name__ == "__main__":

    cola_tickets = deque()

    print("Insertando 3 tickets en la cola: A01, B02, C03")
    cola_tickets.append("A01")
    cola_tickets.append("B02")
    cola_tickets.append("C03")

    print(f"Cantidad de elementos en la cola: {len(cola_tickets)}")
    print(f"Elemento que esta primero: {cola_tickets[0]}")

    for ticket in cola_tickets:
        print(ticket)

    print(f"Extraer un elementdo de la cola: {cola_tickets.popleft()}")
    print(f"Cantidad de elementos en la cola: {len(cola_tickets)}")

    for ticket in cola_tickets:
        print(ticket)
