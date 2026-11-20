import pytest
from flask import Flask
from routes.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_agregar_usuario(client):
    respuesta = client.post('/usuarios', json=
    {
        "nombre": "Juan Perez",
        "cedula": "123456789",
        "correo_electronico": "juan.perez@example.com",
        "telefono": "555-1234",
        "fecha_nacimiento": "1990-01-01"
    })
    assert respuesta.status_code == 201
    datos = respuesta.get_json()
    assert datos["nombre"] == "Juan Perez"
    assert datos["cedula"] == "123456789"
    assert datos["correo_electronico"] == "juan.perez@example.com"
    assert datos["telefono"] == "555-1234"
    assert datos["fecha_nacimiento"] == "1990-01-01"
    assert "id" in datos