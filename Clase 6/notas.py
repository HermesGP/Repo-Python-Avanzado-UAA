from functools import reduce
alumnos = [
    ("Ana", 85),
    ("Luis", 70),
    ("Pedro", 95),
    ("José", 60)
]

# Filtrar los alumnos aprobados (nota >= 70)
aprobados = list(filter(lambda x: x[1] >= 70, alumnos))

# Obtener solo las notas de los alumnos aprobados
notas = list(map(lambda x: x[1], aprobados))

# Obtener la mayor nota entre los alumnos aprobados
mayor = reduce(lambda a, b: max(a, b), notas)

# Ordenar los alumnos por nota de mayor a menor
ordenados = sorted(alumnos, key=lambda x: x[1], reverse=True)

#Asignar calificaciones de 1 a 5 según la nota
def asignar_calificacion(nota):
    if nota >= 90:
        return 5
    elif nota >= 80:
        return 4
    elif nota >= 70:
        return 3
    elif nota >= 60:
        return 2
    else:
        return 1

calificaciones = list(map(lambda x: (x[0], asignar_calificacion(x[1])), alumnos))

# Imprimir los resultados
print("Alumnos aprobados:", aprobados)
print("Notas de los aprobados:", notas)
print("Mayor nota entre los aprobados:", mayor)
print("Alumnos ordenados por nota:", ordenados)
print("Calificaciones asignadas:", calificaciones)
