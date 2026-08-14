#Iterando sobre un diccionario con items() y enumerate()
estudiantes_notas = {"Ana": 90, "Carlos": 75, "Beatriz": 88}

for nombre, nota in estudiantes_notas.items():
    print(f"Estudiante: {nombre} | Nota: {nota}")

print("\n" + "-" * 50 + "\n") 

lenguajes = ["Python", "C#", "JavaScript", "SQL"]

for indice, lenguaje in enumerate(lenguajes):
    print(f"Índice {indice}: {lenguaje}")

print("\n" + "-" * 50 + "\n") 

#Uso de comprensión de listas con diccionarios
notas = {"Ana": 90, "Carlos": 55, "Beatriz": 85, "Diego": 40}

# Filtrar solo los nombres de los alumnos aprobados (nota >= 60)
aprobados = [nombre for nombre, nota in notas.items() if nota >= 60]

print(aprobados)

print("\n" + "-" * 50 + "\n") 

#Hacer una lista de tuplas con los precios con IVA de los productos

productos = {"Thinkpad T14": 300, "Dell Latitude": 225, "HP ProBook": 300}

precios_con_iva = [(producto, precio * 1.1) for producto, precio in productos.items()]

print("\n" + "-" * 50 + "\n") 

#Iterando en orden inverso con reversed()
numeros = [1, 2, 3, 4, 5]

numeros_al_reves = [n for n in reversed(numeros)]

print(numeros_al_reves)

print("\n" + "-" * 50 + "\n") 

#Iterar sobre una secuencia ordenada con sorted()
numeros_desordenados = [42, 12, 89, 7, 23]
print(f"Lista original (sin cambiar): {numeros_desordenados}")
print("Iteración ordenada:")

for num in sorted(numeros_desordenados):
    print(num, end=" ")
print()  # Salto de línea

print("\n" + "-" * 50 + "\n") 

#Creando una lista de listas (matriz) llena de ceros usando comprensión de listas

filas = 3
columnas = 4

matriz = [[0 for _ in range(columnas)] for _ in range(filas)]

for fila in matriz:
    print(fila)

print("\n" + "-" * 50 + "\n") 

#Creando tabla de multiplicar de cualquier número introducido por el usuario usando comprensión de listas

numero_multiplicado = int(input("Introduce un número para generar su tabla de multiplicar: "))

tabla_multiplicar = [numero_multiplicado * i for i in range(1, 11)]

for i, resultado in enumerate(tabla_multiplicar, start=1):
    print(f"{numero_multiplicado} x {i} = {resultado}")
