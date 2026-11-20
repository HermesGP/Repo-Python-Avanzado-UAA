from flask import Flask, jsonify, request

app = Flask(__name__)

# Datos simulados (pueden venir de una base de datos)
alumnos = [
    {"id": 1, "nombre": "Ana", "curso": "Python"},
    {"id": 2, "nombre": "Luis", "curso": "JavaScript"},
    {"id": 3, "nombre": "Marta", "curso": "C#"}
]

# Ruta principal
@app.route('/')
def inicio():
    return "Bienvenido a AlumnosAPI"

# Obtener todos los alumnos
@app.route('/alumnos', methods=['GET'])
def obtener_alumnos():
    return jsonify(alumnos)

# Obtener un alumno por ID
@app.route('/alumnos/<int:id>', methods=['GET'])
def obtener_alumno(id):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    return jsonify(alumno) if alumno else ("Alumno no encontrado", 404)

# Agregar un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def agregar_alumno():
    nuevo = request.get_json()
    nuevo["id"] = max(a["id"] for a in alumnos) + 1
    alumnos.append(nuevo)
    return jsonify(nuevo), 201

# Borrar a un alumno por ID
@app.route('/alumnos/<int:id>', methods=['DELETE'])
def borrar_alumno(id):
    global alumnos
    alumnos = [a for a in alumnos if a["id"] != id]
    return ("Alumno eliminado", 204)

# Actualizar un alumno por ID
@app.route('/alumnos/<int:id>', methods=['PUT'])
def editar_alumno(id):
    datos = request.get_json()
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if alumno:
        alumno.update(datos)
        return jsonify(alumno)
    return ("Alumno no encontrado", 404)

# Usar PATCH para actualizaciones parciales
@app.route('/alumnos/<int:id>', methods=['PATCH'])
def actualizar_alumno(id):
    datos = request.get_json()
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if alumno:
        alumno.update(datos)
        return jsonify(alumno)
    return ("Alumno no encontrado", 404)

if __name__ == '__main__':
    app.run(debug=True)