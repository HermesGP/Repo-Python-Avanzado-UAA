from decimal import Decimal

class Producto:
    def __init__(self, nombre, precio_compra, precio_venta=None):
        self.nombre = nombre
        self.precio_compra = self._convertir_decimal(precio_compra, "precio de compra")
        self.precio_venta = self._convertir_decimal(precio_venta, "precio de venta") if precio_venta is not None else None

    @staticmethod
    def _convertir_decimal(valor, nombre):
        if isinstance(valor, Decimal):
            return valor
        if isinstance(valor, (int, float, str)):
            try:
                return Decimal(str(valor))
            except Exception as exc:
                raise ValueError(f"El {nombre} debe ser un número válido.") from exc
        raise ValueError(f"El {nombre} debe ser un número válido.")

    def __str__(self):
        return f"Producto: {self.nombre}, Precio de compra: {self.precio_compra}, Precio de venta: {self.precio_venta}"

    def calcular_precio_venta(self, margen_ganancia, nivel_impositivo):
        margen_ganancia = self._convertir_decimal(margen_ganancia, "margen de ganancia")
        nivel_impositivo = self._convertir_decimal(nivel_impositivo, "nivel impositivo")

        if margen_ganancia < 0:
            raise ValueError("El margen de ganancia no puede ser negativo.")
        if margen_ganancia > Decimal("30"):
            raise ValueError("El margen de ganancia no puede ser mayor a 30%.")
        if nivel_impositivo not in {Decimal("0"), Decimal("5"), Decimal("10")}:
            raise ValueError("El nivel impositivo debe ser 0, 5 o 10.")

        factor_margen = Decimal("1") + (margen_ganancia / Decimal("100"))
        factor_impositivo = Decimal("1") + (nivel_impositivo / Decimal("100"))
        self.precio_venta = self.precio_compra * factor_margen * factor_impositivo
        return self.precio_venta
if __name__ == "__main__":
    print("Bienvenido al programa de gestión de productos.")
    lista_productos = []
    while True:
        print("\nOpciones:")
        print("1. Agregar producto")
        print("2. Calcular precio de venta")
        print("3. Mostrar productos")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            precio_compra = Decimal(input("Ingrese el precio de compra del producto: "))
            producto = Producto(nombre, precio_compra)
            lista_productos.append(producto)
            print(f"Producto {nombre} agregado con éxito.")
        elif opcion == "2":
            if not lista_productos:
                print("No hay productos en la lista.")
                continue
            for i, producto in enumerate(lista_productos):
                print(f"{i + 1}. {producto.nombre}")
            indice = int(input("Seleccione el número del producto para calcular su precio de venta: ")) - 1
            if 0 <= indice < len(lista_productos):
                margen_ganancia = input("Ingrese el margen de ganancia (%): ")
                nivel_impositivo = input("Ingrese el nivel impositivo (0, 5 o 10): ")
                try:
                    lista_productos[indice].calcular_precio_venta(margen_ganancia, nivel_impositivo)
                    print(f"Precio de venta calculado: {lista_productos[indice].precio_venta}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Índice de producto inválido.")
        elif opcion == "3":
            if not lista_productos:
                print("No hay productos en la lista.")
            else:
                for producto in lista_productos:
                    print(producto)
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")