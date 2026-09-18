#integrador con soporte para ORM (Object-Relational Mapping)
#carga de módulos necesarios para el ORM
from sqlalchemy import create_engine, String,  Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session, DeclarativeBase
from datetime import datetime

cadena_conexion = "mysql+pymysql://hermes:PythonAvanzado@localhost:3306/empleados"

engine = create_engine(cadena_conexion, echo=True)

class Base(DeclarativeBase):
    pass

class Empleado(Base):
    __tablename__ = "empleados"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50))
    apellido: Mapped[str] = mapped_column(String(50))
    edad: Mapped[int] = mapped_column()
    departamento: Mapped[str] = mapped_column(String(50))
    salario: Mapped[Numeric] = mapped_column(Numeric(12,0))
    fecha_ingreso: Mapped[datetime] = mapped_column(DateTime)

#Haciendo la consulta a la base de datos (los datos ya están en la base de datos)
#guardando los datos de la tabla en una lista de diccionarios
def obtener_datos():
    with Session(engine) as session:
        datos = []
        for empleado in session.query(Empleado).all():
            datos.append({
                "id": empleado.id,
                "nombre": empleado.nombre,
                "apellido": empleado.apellido,
                "edad": empleado.edad,
                "departamento": empleado.departamento,
                "salario": empleado.salario,
                "fecha_ingreso": empleado.fecha_ingreso
            })
    return datos

#aplicando pipeline con map y filter en donde se sube en un 10% el salario de los empleados de Márketing
def aumentar_salario_marketing(datos):
    #filter para obtener solo los empleados de Marketing
    marketing = filter(lambda x: x["departamento"] == "Marketing", datos)
    #map para aumentar el salario en un 10%
    marketing_actualizado = map(lambda x: {**x, "salario": x["salario"] * 1.1}, marketing)
    return list(marketing_actualizado)

#funcion para guardar los datos cambiados en la base de datos
def guardar_datos(datos):
    with Session(engine) as session:
        for dato in datos:
            empleado = session.query(Empleado).filter(Empleado.id == dato["id"]).first()
            if empleado:
                empleado.nombre = dato["nombre"]
                empleado.apellido = dato["apellido"]
                empleado.edad = dato["edad"]
                empleado.departamento = dato["departamento"]
                empleado.salario = dato["salario"]
                empleado.fecha_ingreso = dato["fecha_ingreso"]
        session.commit()

if __name__ == "__main__":
    datos = obtener_datos()
    marketing_actualizado = aumentar_salario_marketing(datos)
    guardar_datos(marketing_actualizado)
    print("Salarios de Marketing actualizados correctamente.")