#importando los módulos necesarios
from functools import reduce
from datetime import datetime
from pathlib import Path
from decimal import Decimal
import csv
import time

#decorador para medir el tiempo de ejecución de una función
def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {fin - inicio} segundos")
        return resultado
    return wrapper

#función para imprimir los registros en pantalla
def imprimir_registros(datos):
    for registro in datos:
        print(registro)

#ordena los registros por salario de manera descendente
@medir_tiempo
def ordenar_por_salario_desc(datos):
    return sorted(datos, key=lambda x: x.get("salario", 0), reverse=True)

#pipeline para convertir los valores numéricos a entero, los salarios a Decimal y las fechas a datetime
@medir_tiempo
def convertir_numericos(datos):
    datos_map = list(map(lambda x: {k: int(v) if v.isdigit() else v for k, v in x.items()}, datos))
    #el operador **x permite mantener el resto de los campos del diccionario sin modificarlos
    #map: convertir los valores de las columnas numéricas a entero
    datos_map = list(map(lambda x: {**x, "salario": Decimal(x["salario"]) if "salario" in x else x.get("salario")}, datos_map))
    #map: convertir las fechas a datetime
    datos_map = list(map(lambda x: {**x, "fecha": datetime.strptime(x["fecha"], "%Y-%m-%d") if "fecha" in x else x.get("fecha")}, datos_map))
    return datos_map

#pipeline de funciones con map y filter
@medir_tiempo
def pipeline(datos):
    #filter: filtrar los registros donde el departamento sea "Sistemas"
    datos_filter_sistemas = list(filter(lambda x: x["departamento"] == "Sistemas", datos))
    #map: aumentar todos los salarios del departamento de sistemas en un 15%
    datos_map_sistemas = list(map(lambda x: {**x, "salario": x["salario"] * Decimal("1.15")}, datos_filter_sistemas))
    return datos_map_sistemas

#darme la suma de los salarios con reduce
@medir_tiempo
def suma_salarios(datos):
    return reduce(lambda acc, x: acc + x["salario"], datos, Decimal("0"))

#main donde se aplican las funciones definidas
if __name__ == "__main__":
    #guardando los datos de dataset.csv en una lista de diccionarios
    ruta_csv = Path(__file__).resolve().with_name("dataset.csv")
    datos = []
    with open(ruta_csv, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            datos.append(fila)

    #convertir los datos a los tipos adecuados
    datos_convertidos = convertir_numericos(datos)
    datos_ordenados = ordenar_por_salario_desc(datos_convertidos)
    imprimir_registros(datos_ordenados)

    #aplicar el pipeline de funciones con map y filter
    resultado_pipeline = pipeline(datos_convertidos)
    imprimir_registros(resultado_pipeline)

    #calcular la suma de los salarios del resultado del pipeline
    suma = suma_salarios(resultado_pipeline)
    print(f"Suma de los salarios: {suma}")