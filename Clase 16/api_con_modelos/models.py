class Usuario:
    def __init__(self, id, nombre, cedula, email):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.email = email
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "email": self.email
        }