import time
from concurrent.futures import ThreadPoolExecutor

import requests

URLS = [
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.github.com",
    "https://www.mozilla.org",
    "https://httpbin.org/delay/1",
]


def solicitar(url):
    """Descarga una página y devuelve su tamaño en bytes."""
    try:
        respuesta = requests.get(url, timeout=10)
        return len(respuesta.content)
    except requests.RequestException:
        return 0


def secuencial_solicitudes(urls):
    return [solicitar(url) for url in urls]


def hilos_solicitudes(urls, hilos):
    with ThreadPoolExecutor(max_workers=hilos) as executor:
        return list(executor.map(solicitar, urls))


def medir(nombre, funcion, *args):
    inicio = time.time()
    resultado = funcion(*args)
    duracion = time.time() - inicio
    print(f"{nombre:<30} {duracion:8.3f} s")
    return resultado, duracion


def comparar(titulo, nombre_seq, f_seq, nombre_par, f_par, datos, hilos):
    print(f"\n=== {titulo} ===")
    _, t_seq = medir(nombre_seq, f_seq, datos)
    _, t_par = medir(nombre_par, f_par, datos, hilos)
    print(f"Speedup: {t_seq / t_par:.2f}x")


if __name__ == "__main__":
    comparar("Solicitudes HTTP (5 páginas)",
             "Secuencial", secuencial_solicitudes,
             "ThreadPoolExecutor", hilos_solicitudes, URLS, len(URLS))
