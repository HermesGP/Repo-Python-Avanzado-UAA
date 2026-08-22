from pathlib import Path

while True:
    try:
        numero = int(input("Ingrese un número entero: "))
        break
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número entero.")

nombre_archivo = Path(__file__).resolve().with_name("tabla_multiplicar.txt")
try:
    with open(nombre_archivo, "w") as archivo:
        archivo.write(f"Tabla de multiplicar del {numero}:\n")
        for i in range(1, 11):
            resultado = numero * i
            archivo.write(f"{numero} x {i} = {resultado}\n")
except IOError:
    print(f"No se pudo escribir en el archivo '{nombre_archivo}'.")
else:
    print(f"Tabla de multiplicar del {numero} guardada en '{nombre_archivo}'.")
finally:
    print("Programa finalizado.")