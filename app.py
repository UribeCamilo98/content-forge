from flask import Flask, render_template, request
from generator.carousel import Carrusel
from utils.colors import obtener_paleta

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar():
    texto = request.form["texto"]
    nombre_paleta = request.form.get("paleta", "oscuro")
    paleta = obtener_paleta(nombre_paleta)
    plantilla = Carrusel(texto, paleta["fondo"], paleta["texto"])
    ruta = plantilla.generar()

    return render_template("index.html", ruta = ruta)

if __name__ == "__main__":
    app.run(debug=True)