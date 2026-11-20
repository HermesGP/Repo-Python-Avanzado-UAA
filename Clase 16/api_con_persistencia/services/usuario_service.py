from models.usuario import Usuario

def agregar_usuario(usuario_dao, usuario):
    usuario_dao.agregar(usuario)

def obtener_usuario(usuario_dao, usuario_id):
    return usuario_dao.obtener(usuario_id)

def obtener_todos_usuarios(usuario_dao):
    return usuario_dao.obtener_todos()

def buscar_usuarios_por_nombre(usuario_dao, nombre):
    return usuario_dao.buscar_por_nombre(nombre)

def actualizar_usuario(usuario_dao, usuario):
    usuario_dao.actualizar(usuario)

def eliminar_usuario(usuario_dao, usuario):
    usuario_dao.eliminar(usuario)