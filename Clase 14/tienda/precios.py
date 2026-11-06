from decimal import Decimal

def aplicar_descuento(precio: Decimal, porcentaje: float) -> Decimal:
    if precio < 0:
        raise ValueError("El precio no puede ser negativo")
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError("El porcentaje debe estar entre 0 y 100")

    return precio - (precio * porcentaje / 100)


def calcular_impuesto(precio: Decimal, porcentaje_impuesto: float) -> Decimal:
    if precio < 0:
        raise ValueError("El precio no puede ser negativo")
    if porcentaje_impuesto < 0:
        raise ValueError("El impuesto no puede ser negativo")

    return precio * porcentaje_impuesto / 100


def calcular_total(precio: Decimal, descuento: float, impuesto: float) -> Decimal:
    precio_con_descuento = aplicar_descuento(precio, descuento)
    importe_impuesto = calcular_impuesto(precio_con_descuento, impuesto)
    return precio_con_descuento + importe_impuesto