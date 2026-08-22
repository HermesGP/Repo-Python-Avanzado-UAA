import csv
from pathlib import Path

# Construye la ruta desde la ubicacion de este script.
ruta_csv = Path(__file__).resolve().with_name("nomina.csv")

with ruta_csv.open("r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    for columna, fila in enumerate(lector):
        print(
            f"Fila {columna + 1}: {fila['nombre']} {fila['apellido']} - "
            f"Edad: {fila['edad']} - Departamento: {fila['departamento']} - "
            f"Salario: {fila['salario']} - Fecha de ingreso: {fila['fecha_ingreso']}"
        )
#Ejemplo de filtrado de empleados de la sección de Sistemas con salario mayor a 6000000
with ruta_csv.open("r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    print("\nEmpleados de la sección de Sistemas con salario mayor a 6000000:")
    for fila in lector:
        if fila["departamento"] == "Sistemas" and int(fila["salario"]) > 6000000:
            print(
                f"{fila['nombre']} {fila['apellido']} - "
                f"Edad: {fila['edad']} - Salario: {fila['salario']} - "
                f"Fecha de ingreso: {fila['fecha_ingreso']}"
            )

#Calculo del salario promedio por seccion
secciones = [
    "Administración",
    "Marketing",
    "Finanzas",
    "Gerencia",
    "Recursos Humanos",
    "Sistemas"
]
for seccion in secciones:
    with ruta_csv.open("r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        salarios = [int(fila["salario"]) for fila in lector if fila["departamento"] == seccion]
        if salarios:
            promedio = sum(salarios) / len(salarios)
            print(f"Salario promedio en {seccion}: {promedio:.2f}")
        else:
            print(f"No hay empleados en la sección de {seccion}.")