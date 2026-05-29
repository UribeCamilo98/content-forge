from flask import Flask, render_template, request, send_file
from generator.carousel import Carrusel
from utils.colors import obtener_paleta, PALETAS
from utils.fonts import font_manager
from config import PRESETS_TAMANO, TAMANO_OPCIONES
import io

def hex_a_rgb(h):
    h = h.lstrip("#")
    return tuple(
        int(h[i:i+2], 16)
        for i in (0, 2, 4)
    )

app = Flask(__name__)
@app.route("/")
def home():
    fuentes = font_manager.listar_fuentes()
    return render_template("index.html", fuentes=fuentes, tamano_opciones=TAMANO_OPCIONES, paletas=PALETAS)

@app.route("/generar", methods=["POST"])
def generar():
    texto = request.form["texto"]
    color_fondo_hex = request.form.get("color_fondo", "")
    color_texto_hex = request.form.get("color_texto", "")

    if not color_fondo_hex or not color_texto_hex:
        nombre_paleta = request.form.get("paleta", "oscuro")
        paleta = obtener_paleta(nombre_paleta)
        color_fondo_hex = paleta["fondo"]
        color_texto_hex = paleta["texto"]

    color_fondo = hex_a_rgb(color_fondo_hex)
    color_texto = hex_a_rgb(color_texto_hex)

    fuente = request.form.get("fuente", "")
    tamano_str = request.form.get("tamano", "")
    alineacion = request.form.get("alineacion", "centro")
    tamano = int(tamano_str) if tamano_str else None

    preset = request.form.get("preset_tamano", "cuadrado")
    ancho,alto = PRESETS_TAMANO.get(preset, PRESETS_TAMANO["cuadrado"])
    num_slides_str = request.form.get("num_slides", "")
    num_slides = int(num_slides_str) if num_slides_str else None

    borde_activar= request.form.get("borde_activar")
    if borde_activar:
        contorno_color = hex_a_rgb(request.form.get("borde_color", "#000000"))
        contorno_grosor = int(request.form.get("borde_grosor", 3))
    else:
        contorno_color = None
        contorno_grosor= 3

    sombra_activar = request.form.get("sombra_activar")
    if sombra_activar:
        sx = int(request.form.get("sombra_offset_x", 5))
        sy = int(request.form.get("sombra_offset_y", 5))
        sombra_offset = (sx, sy)
        sombra_color = hex_a_rgb(request.form.get("sombra_color", "#808080"))
    else:
        sombra_offset = None
        sombra_color = (128, 128, 128)

    plantilla = Carrusel(texto, color_fondo, color_texto, fuente=fuente, 
                         num_slides=num_slides, tamano=tamano, alineacion=alineacion, 
                         ancho=ancho, alto=alto, contorno_color=contorno_color,
                         contorno_grosor=contorno_grosor, sombra_offset=sombra_offset,
                         sombra_color=sombra_color)
    ruta = plantilla.generar()

    return render_template("index.html", ruta = ruta, fuentes=font_manager.listar_fuentes(), 
                           tamano_opciones=TAMANO_OPCIONES, paletas=PALETAS)

@app.route("/preview", methods= ["POST"])
def preview():
    texto= request.form["texto"]
    color_fondo_hex = request.form.get("color_fondo", "")
    color_texto_hex = request.form.get("color_texto", "")

    if not color_fondo_hex or not color_texto_hex:
        nombre_paleta = request.form.get("paleta", "oscuro")
        paleta = obtener_paleta(nombre_paleta)
        color_fondo_hex = paleta["fondo"]
        color_texto_hex = paleta["texto"]

    color_fondo = hex_a_rgb(color_fondo_hex)
    color_texto = hex_a_rgb(color_texto_hex)

    fuente = request.form.get("fuente", "")
    tamano_str = request.form.get("tamano", "")
    alineacion = request.form.get("alineacion", "centro")
    tamano = int(tamano_str) if tamano_str else None

    preset = request.form.get("preset_tamano", "cuadrado")
    ancho, alto = PRESETS_TAMANO.get(preset, PRESETS_TAMANO["cuadrado"])
    num_slides_str = request.form.get("num_slides", "")
    num_slides = int(num_slides_str) if num_slides_str else None

    borde_activar = request.form.get("borde_activar")
    if borde_activar:
        contorno_color = hex_a_rgb(request.form.get("borde_color", "#000000"))
        contorno_grosor = int(request.form.get("borde_grosor", 3))
    else:
        contorno_color = None
        contorno_grosor = 3
    
    sombra_activar = request.form.get("sombra_activar")
    if sombra_activar:
        sx = int(request.form.get("sombra_offset_x", 5))
        sy = int(request.form.get("sombra_offset_y", 5))
        sombra_offset = (sx, sy)
        sombra_color = hex_a_rgb(request.form.get("sombra_color", "#808080"))
    else:
        sombra_offset = None
        sombra_color = (128, 128, 128)

    slide_index = int(request.form.get("slide_index", 0))

    plantilla = Carrusel(
        texto, color_fondo, color_texto, fuente=fuente,
        num_slides=num_slides, tamano=tamano, alineacion=alineacion,
        ancho=ancho, alto=alto, contorno_color=contorno_color,
        contorno_grosor=contorno_grosor, sombra_offset=sombra_offset,
        sombra_color=sombra_color
    )
    img = plantilla.render_slide(slide_index)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    resp = send_file(buf, mimetype="image/png")
    resp.headers["X-Total-Slides"] = str(len(plantilla.textos))
    return resp


if __name__ == "__main__":
    app.run(debug=True)