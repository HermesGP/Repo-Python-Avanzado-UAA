class Vehiculo:
    def __init__(self, marca, modelo, color, año, precio, origen, registro=None, disponible=True):
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.año = año
        self.precio = precio
        self.origen = origen
        self.registro = registro
        self.disponible = disponible


    def obtener_ficha_tecnica(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Color: {self.color}, Año: {self.año}, Precio: {self.precio}, Origen: {self.origen}, Registro: {self.registro} Disponible: {self.disponible}"

class Auto(Vehiculo):
    def __init__(self, marca, modelo, color, año, precio, origen, tipo_combustible, numero_chasis, numero_motor, tipo_traccion, registro=None, disponible=True):
        super().__init__(marca, modelo, color, año, precio, origen, registro, disponible)
        self.tipo_combustible = tipo_combustible
        self.numero_chasis = numero_chasis
        self.numero_motor = numero_motor
        self.tipo_traccion = tipo_traccion
def obtener_ficha_tecnica(self):
    return super().obtener_ficha_tecnica() + f", Combustible: {self.tipo_combustible}, No. de chasis (VIN): {self.numero_chasis}, No. de motor: {self.numero_motor}, Tipo de tracción: {self.tipo_traccion}"

class Moto(Vehiculo):
    def __init__(self, marca, modelo, color, año, precio, origen, tipo_combustible, numero_cuadro, numero_motor, cilindrada, registro=None, disponible=True):
        super().__init__(marca, modelo, color, año, precio, origen, registro, disponible)
        self.tipo_combustible = tipo_combustible
        self.numero_cuadro = numero_cuadro
        self.numero_motor = numero_motor
        self.tipo_cilindrada = cilindrada

    def obtener_ficha_tecnica(self):
        return super().obtener_ficha_tecnica() + f", Combustible: {self.tipo_combustible}, No. de cuadro: {self.numero_cuadro}, NNo. de motor: {self.numero_motor}, Cilindrada: {self.tipo_cilindrada} cc"
class Barco(Vehiculo):
    def __init__(self, marca, modelo, color, año, precio, origen, nombre_embarcacion, eslora_metros, potencia_hp, tipo_motor, registro=None, disponible=True):
        super().__init__(marca, modelo, color, año, precio, origen, registro, disponible)
        self.nombre_embarcacion = nombre_embarcacion
        self.eslora_metros = eslora_metros
        self.potencia_hp = potencia_hp
        self.tipo_motor = tipo_motor

    def obtener_ficha_tecnica(self):
        return super().obtener_ficha_tecnica() + f", Nombre de la embarcación: {self.nombre_embarcacion}, Eslora: {self.eslora_metros} m, Potencia: {self.potencia_hp} HP, Tipo de motor: {self.tipo_motor}"
if __name__ == "__main__":
    hilux = Auto("Toyota", "Hilux", "Blanco", 2022, 35000, "Importado", "Diésel", "1234567890ABCDEF1", "9876543210ZYXWVU1", "4x4")
    vitz = Auto("Toyota", "Vitz", "Rojo", 2021, 20000, "Importado", "Nafta", "1234567890ABCDEF2", "9876543210ZYXWVU2", "FWD")
    kenton = Moto("Honda", "GTR 150", "Negro", 2023, 8000, "Nacional", "Nafta", "94P1234567890ABCD", "157FMI987654", 150)
    barquito = Barco("Tracker","Pro Guide 175", "Blanco", 2024, 20000, "Importado", "Barquito Lindo", 5.4, 90, "Fuera de Borda")
    inventario = [hilux, vitz, kenton, barquito]
    for item in inventario:
        print("-------------------------------------------\n")
        print(item.obtener_ficha_tecnica())