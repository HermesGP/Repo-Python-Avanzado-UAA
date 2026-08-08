from abc import abstractmethod
from enum import Enum
class Animal:
    def __init__(self, id, nombre, edad):
        self.id = id
        self.nombre = nombre
        self.edad = edad
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("El id debe ser un número entero.")
        self._id = value
    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("El nombre debe ser una cadena de texto.")
        elif len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = value
    @property
    def edad(self):
        return self._edad
    @edad.setter
    def edad(self, value):
        if not isinstance(value, int):
            raise ValueError("La edad debe ser un número entero.")
        elif value < 0:
            raise ValueError("La edad no puede ser negativa.")
        self._edad = value
    @abstractmethod
    def descripcion(self):
        pass
    @abstractmethod
    def sonido(self):
        pass
class Tipos_Perro(Enum):
    PEQUENO = "Pequeño"
    MEDIANO = "Mediano"
    GRANDE = "Grande"
class Perro(Animal):
    def __init__(self, id, nombre, edad, raza, tipo):
        super().__init__(id, nombre, edad)
        self.raza = raza
        self.tipo = tipo
    @property
    def raza(self):
        return self._raza
    @raza.setter
    def raza(self, value):
        if not isinstance(value, str):
            raise ValueError("La raza debe ser una cadena de texto.")
        elif len(value) < 3:
            raise ValueError("La raza debe tener al menos 3 caracteres.")
        self._raza = value
    def descripcion(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Edad: {self.edad}, Raza: {self.raza}, Tipo: {self.tipo.value}"
    @property
    def tipo(self):
        return self._tipo
    @tipo.setter
    def tipo(self, value):
        if not isinstance(value, Tipos_Perro):
            raise ValueError("No es un tipo válido de Perro")
        self._tipo = value
    def sonido(self):
        return "Guau"
class Gato(Animal):
    def __init__(self, id, nombre, edad, color):
        super().__init__(id, nombre, edad)
        self.color = color
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise ValueError("El color debe ser una cadena de texto.")
        elif len(value) < 3:
            raise ValueError("El color debe tener al menos 3 caracteres.")
        self._color = value
    def descripcion(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Edad: {self.edad}, Color: {self.color}"
    def sonido(self):
        return "Miau"
if __name__ == "__main__":
    perro1 = Perro(1, "Firulais", 3, "Labrador", Tipos_Perro.GRANDE)
    print(perro1.descripcion())
    print(perro1.sonido())
    gato1 = Gato(2, "Mittens", 2, "Negro")
    print(gato1.descripcion())
    print(gato1.sonido())
