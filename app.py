from flask import Flask
from generator.base import PlantillaBase
from utils.colors import obtener_paleta
from config import COLOR_FONDO, COLOR_TEXTO

app = Flask (__name__)
@app.route("/")
def home():
    return "Hola Mundo"

@app.route("/generar")
def generar():
    texto = "MONDONGO"
    paleta = obtener_paleta("pastel")
    plantilla = PlantillaBase(texto, paleta["fondo"],paleta["texto"])
    ruta = plantilla.generar()
    return f"imagen generada: {ruta}"

if __name__ == "__main__":
    app.run(debug=True)