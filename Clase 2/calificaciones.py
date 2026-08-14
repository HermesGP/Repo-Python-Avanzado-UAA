#Lista de diccionarios de los alumnos con sus calificaciones
alumnos = [{"nombre": "Ana", "primer parcial": 90, "segundo parcial": 85, "examen final": 92},
           {"nombre": "Carlos", "primer parcial": 55, "segundo parcial": 60, "examen final": 58},
           {"nombre": "Beatriz", "primer parcial": 85, "segundo parcial": 88, "examen final": 90},
           {"nombre": "Diego", "primer parcial": 40, "segundo parcial": 50, "examen final": 45}]

#calculando la calificación final de cada alumno y agregándola al diccionario
for alumno in alumnos:
    calificacion_final = (alumno["primer parcial"] * 0.25 + alumno["segundo parcial"] * 0.25 + alumno["examen final"]* 0.5)
    alumno["calificación final"] = round(calificacion_final, 2)

#imprimiendo la lista de diccionarios con las calificaciones finales
for alumno in alumnos:
    print(f"Nombre: {alumno["nombre"]}")
    match alumno["calificación final"]:
        case calificacion if calificacion >= 90:
            print(f"Calificación final: {alumno["calificación final"]} - 5 - Excelente")
        case calificacion if calificacion >= 80:
            print(f"Calificación final: {alumno["calificación final"]} - 4 - Muy Bien")
        case calificacion if calificacion >= 70:
            print(f"Calificación final: {alumno["calificación final"]} - 3 - Bien")
        case calificacion if calificacion >= 60:
            print(f"Calificación final: {alumno["calificación final"]} - 2 - Suficiente")
        case _:
            print(f"Calificación final: {alumno["calificación final"]} - 1 - Insuficiente")
