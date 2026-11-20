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
    response = client.post('/usuarios', json={
        "nombre": "Juan Perez",
        "cedula": "123456789",
        "correo_electronico": "juan.perez@example.com",
        "telefono": "555-1234",
        "fecha_nacimiento": "1990-01-01"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["nombre"] == "Juan Perez"
    assert data["cedula"] == "123456789"
    assert data["correo_electronico"] == "juan.perez@example.com"
    assert data["telefono"] == "555-1234"
    assert data["fecha_nacimiento"] == "1990-01-01"
    assert "id" in data

def test_agregar_usuario_invalido(client):
    response = client.post('/usuarios', json={
        "nombre": "",
        "cedula": "",
        "correo_electronico": "invalid-email",
        "telefono": "",
        "fecha_nacimiento": "invalid-date"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert isinstance(data["error"], str)


