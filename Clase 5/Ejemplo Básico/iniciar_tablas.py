from database import Base, engine
import models

#Borramos todas las tablas
Base.metadata.drop_all(engine)
#Creamos todas las tablas
Base.metadata.create_all(engine)
