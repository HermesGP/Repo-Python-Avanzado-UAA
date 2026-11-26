from flask import Flask, render_template, abort
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Datos de ejemplo
cursos = [
    {
        "id": 1,
        "nombre": "Python",
        "profesor": "Carlos Benítez",
        "duracion": 40,
        "nivel": "Inicial",
        "descripcion": "Introducción a la programación con Python.",
        "activo": True
    },
    {
        "id": 2,
        "nombre": "Bases de Datos",
        "profesor": "Ana González",
        "duracion": 30,
        "nivel": "Intermedio",
        "descripcion": "Diseño y consultas utilizando SQL.",
        "activo": True
    },
    {
        "id": 3,
        "nombre": "Desarrollo Web",
        "profesor": "Pedro Ramírez",
        "duracion": 50,
        "nivel": "Avanzado",
        "descripcion": "Desarrollo de aplicaciones web con Flask.",
        "activo": False
    }
]

@app.route("/")
def index():
    return render_template("index.html", cursos=cursos)

@app.route("/curso/<int:curso_id>")
def curso(curso_id):
    curso = next((c for c in cursos if c["id"] == curso_id), None)
    if curso is None:
        abort(404)
    return render_template("detalle.html", curso=curso)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])