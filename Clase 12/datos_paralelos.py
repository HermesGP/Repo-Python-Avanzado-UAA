import math
import random
import time
from multiprocessing import Pool, cpu_count


def operacion_paralelizable(n):
    """Costosa e independiente por elemento: ideal para paralelizar."""
    total = 0.0
    for i in range(1, 300):
        total += math.sqrt(n + i) * math.sin(n * i) + math.log(n + i)
    return total


def operacion_dependiente(lista):
    """Cada paso depende del resultado anterior: no se puede paralelizar."""
    acumulado = 1.0
    for n in lista:
        acumulado = math.sin(acumulado + n) * math.sqrt(abs(acumulado) + n) + 1.0
    return acumulado


def secuencial_paralelizable(datos):
    return [operacion_paralelizable(n) for n in datos]


def pool_paralelizable(datos, procesos):
    with Pool(processes=procesos) as pool:
        return pool.map(operacion_paralelizable, datos)


def pool_dependiente(datos, procesos):
    # Cada bloque depende del resultado del anterior, así que dividirlo
    # no da el valor correcto y solo añade sobrecarga (envío de datos).
    tam = math.ceil(len(datos) / procesos)
    bloques = [datos[i:i + tam] for i in range(0, len(datos), tam)]
    with Pool(processes=procesos) as pool:
        return pool.map(operacion_dependiente, bloques)


def medir(nombre, funcion, *args):
    inicio = time.time()
    resultado = funcion(*args)
    duracion = time.time() - inicio
    print(f"{nombre:<30} {duracion:8.3f} s")
    return resultado, duracion


def comparar(titulo, nombre_seq, f_seq, nombre_par, f_par, datos, procesos):
    print(f"\n=== {titulo} ===")
    _, t_seq = medir(nombre_seq, f_seq, datos)
    _, t_par = medir(nombre_par, f_par, datos, procesos)
    print(f"Speedup: {t_seq / t_par:.2f}x")


def secuencial_dependiente(datos, _procesos=None):
    return operacion_dependiente(datos)


if __name__ == "__main__":
    procesos = cpu_count()
    random.seed(42)
    print(f"Procesos: {procesos}")

    datos = [random.randint(1, 10_000) for _ in range(200_000)]
    comparar("PARALELIZABLE (elementos independientes)",
             "Secuencial", lambda d, *_: secuencial_paralelizable(d),
             "Pool.map", pool_paralelizable, datos, procesos)

    datos_dep = [random.randint(1, 10_000) for _ in range(3_000_000)]
    comparar("NO paralelizable (dependencia secuencial)",
             "Secuencial", lambda d, *_: operacion_dependiente(d),
             "Pool.map por bloques", pool_dependiente, datos_dep, procesos)
