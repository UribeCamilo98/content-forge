from flask import Flask, render_template, request
from generator.carousel import Carrusel
from utils.colors import obtener_paleta
from utils.fonts import font_manager

app = Flask(__name__)
@app.route("/")
def home():
    fuentes = font_manager.listar_fuentes()
    return render_template("index.html", fuentes=fuentes)

@app.route("/generar", methods=["POST"])
def generar():
    texto = request.form["texto"]
    nombre_paleta = request.form.get("paleta", "oscuro")
    paleta = obtener_paleta(nombre_paleta)

    fuente = request.form.get("fuente", "")
    tamano_str = request.form.get("tamano", "")
    alineacion = request.form.get("alineacion", "centro")
    tamano = int(tamano_str) if tamano_str else None

    plantilla = Carrusel(texto, paleta["fondo"], paleta["texto"], fuente=fuente, tamano=tamano, alineacion=alineacion)
    ruta = plantilla.generar()

    return render_template("index.html", ruta = ruta, fuentes=font_manager.listar_fuentes())

if __name__ == "__main__":
    app.run(debug=True)