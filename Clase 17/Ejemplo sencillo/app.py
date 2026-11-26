from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

peliculas_favoritas = ["El Señor de los Anillos: La Comunidad del Anillo", "Star Wars Episodio V: El Imperio Contraataca","Inception", "Interstellar"]
libros_favoritos = ["Cien Años de Soledad", "Don Quijote de la Mancha", "1984", "El Principito"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libros')
def libros():
    return render_template('libros.html', libros=libros_favoritos)

@app.route('/peliculas')
def peliculas():
    return render_template('peliculas.html', peliculas=peliculas_favoritas)

if __name__ == '__main__':
    app.run(debug=True)