def normalizar_nombre(nombre: str) -> str:
    return nombre.strip().title()


def validar_producto(nombre: str, precio: float) -> dict:
    if not nombre or not nombre.strip():
        raise ValueError("El nombre del producto es obligatorio")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que cero")

    return {
        "nombre": normalizar_nombre(nombre),
        "precio": precio,
    }