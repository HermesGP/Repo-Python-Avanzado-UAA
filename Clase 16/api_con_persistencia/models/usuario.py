from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import date
from database.config import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50))
    cedula: Mapped[str] = mapped_column(String(20))
    correo_electronico: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    fecha_nacimiento: Mapped[date] = mapped_column()

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "correo_electronico": self.correo_electronico,
            "telefono": self.telefono,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None
        }