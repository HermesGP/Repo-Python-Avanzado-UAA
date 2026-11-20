from flask import Flask
from routes.routes import routes
from database.config import Base, engine

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    # Crear conexión y tabla al iniciar la aplicación
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    app.run(debug=True)