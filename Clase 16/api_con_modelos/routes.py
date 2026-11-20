from data import usuarios
from flask import Blueprint, jsonify, request
from models import Usuario

# El Blueprint permite organizar las rutas en módulos para usar en la app principal
routes = Blueprint('routes', __name__)

# Ruta principal
@routes.route('/')
def inicio():
    return "Bienvenido a la API de usuarios"

# Obtener todos los usuarios
@routes.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify([u.to_dict() for u in usuarios])

# Obtener un usuario por ID
@routes.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = next((u for u in usuarios if u.id == id), None)
    return jsonify(usuario.to_dict()) if usuario else ("Usuario no encontrado", 404)

# Agregar un nuevo usuario
@routes.route('/usuarios', methods=['POST'])
def agregar_usuario():
    datos = request.get_json()
    nuevo = Usuario(len(usuarios) + 1, datos["nombre"], datos["cedula"], datos["email"])
    usuarios.append(nuevo)
    return jsonify(nuevo.to_dict()), 201

# Borrar un usuario por ID
@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def borrar_usuario(id):
    global usuarios
    usuarios = [u for u in usuarios if u.id != id]
    return ("Usuario eliminado", 204)

# Actualizar un usuario por ID
@routes.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    datos = request.get_json()
    usuario = next((u for u in usuarios if u.id == id), None)
    if usuario:
        usuario.nombre = datos.get("nombre", usuario.nombre)
        usuario.cedula = datos.get("cedula", usuario.cedula)
        usuario.email = datos.get("email", usuario.email)
        return jsonify(usuario.to_dict())
    return ("Usuario no encontrado", 404)

