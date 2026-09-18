#Medir el tiempo de ejecución de una función usando un decorador
import time

def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {fin - inicio} segundos")
        return resultado
    return wrapper

#Medir una suma de 100 numeros
@medir_tiempo
def suma_100_numeros():
    return sum(range(1, 101))

# Llamar a la función para medir su tiempo de ejecución
suma_100_numeros()

#Medir una función matemática complicada (potencia de suma de cubos de funciones trigonométricas)
import math

@medir_tiempo
def potencia_suma_cubos_trig(n):
    return sum((math.sin(i) ** 3 + math.cos(i) ** 3) ** 2 for i in range(1, n + 1))

# Llamar a la función para medir su tiempo de ejecución
potencia_suma_cubos_trig(10000)

#la misma función con asincronía
import asyncio

@medir_tiempo
async def potencia_suma_cubos_trig_async(n):
    return sum((math.sin(i) ** 3 + math.cos(i) ** 3) ** 2 for i in range(1, n + 1))

# Llamar a la función asincrónica para medir su tiempo de ejecución
asyncio.run(potencia_suma_cubos_trig_async(10000))

