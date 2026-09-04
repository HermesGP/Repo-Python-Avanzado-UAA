from database import Base, engine
import models
from consulta_insert import consulta_insert
from consulta_select import consulta_select

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    consulta_insert()
    consulta_select()