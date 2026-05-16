from flask import Flask
from generator.carousel import Carrusel
from utils.colors import obtener_paleta

app = Flask (__name__)
@app.route("/")
def home():
    return "Hola Mundo"

@app.route("/generar")
def generar():
    texto = """Yo no quiero morirme sin saber de tu boca.
Yo no quiero morirme con el alma perpleja
sabiéndote distinto, perdido en otras playas.

Yo no quiero morirme con este desconsuelo
por el arco infinito de esa cúpula triste
donde habitan tus sueños al sol de mediodía.

Yo no quiero morirme sin haberte entregado
las doradas esferas de mi cuerpo,
la piel que me recubre, el temblor que me invade.

Yo no quiero morirme sin que me hayas amado."""
    paleta = obtener_paleta("vibrante")
    plantilla = Carrusel(texto, paleta["fondo"], paleta["texto"], num_slides=20)
    
    ruta = plantilla.generar()

    return f"Carrusel generado en: {ruta}"

if __name__ == "__main__":
    app.run(debug=True)