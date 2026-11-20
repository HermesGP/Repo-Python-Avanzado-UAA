from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from services import usuario_service as service
from DAOs.usuario_dao import UsuarioDAO

usuario_dao = UsuarioDAO()
routes = Blueprint('routes', __name__)

@routes.route('/')
def inicio():
    return "Bienvenido a la API de usuarios"

@routes.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = service.obtener_todos_usuarios(usuario_dao)
    return jsonify([u.to_dict() for u in usuarios])

@routes.route('/usuarios/buscar/<nombre>', methods=['GET'])
def buscar_usuario(nombre):
    usuarios = [u for u in service.buscar_usuarios_por_nombre(usuario_dao, nombre)]
    return jsonify([u.to_dict() for u in usuarios])

@routes.route('/usuarios', methods=['POST'])
def agregar_usuario():
    datos = request.get_json()
    nuevo = Usuario()
    nuevo.nombre = datos.get('nombre')
    nuevo.cedula = datos.get('cedula')
    nuevo.correo_electronico = datos.get('correo_electronico')
    nuevo.telefono = datos.get('telefono')
    nuevo.fecha_nacimiento = datos.get('fecha_nacimiento')
    service.agregar_usuario(usuario_dao,nuevo)
    return jsonify(nuevo.to_dict()), 201

@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def borrar_usuario(id):
    usuario = service.obtener_usuario(usuario_dao, id)
    if usuario:
        service.eliminar_usuario(usuario_dao, usuario)
        return ("Usuario eliminado", 204)
    return ("Usuario no encontrado", 404)

@routes.route('/usuarios/<int:id>', methods=['PATCH'])
def editar_usuario(id):
    datos = request.get_json()
    usuario = service.obtener_usuario(usuario_dao, id)
    if usuario:
        usuario.nombre = datos.get('nombre', usuario.nombre)
        usuario.cedula = datos.get('cedula', usuario.cedula)
        usuario.correo_electronico = datos.get("correo_electronico", usuario.correo_electronico)
        usuario.telefono = datos.get("telefono", usuario.telefono)
        usuario.fecha_nacimiento = datos.get("fecha_nacimiento", usuario.fecha_nacimiento)
        service.actualizar_usuario(usuario_dao, usuario)
        return jsonify(usuario.to_dict())
    return ("Usuario no encontrado", 404)

