import io
import zipfile
from datetime import datetime
from PIL import Image
from flask import Flask, render_template, request, send_file
from generator.carousel import Carrusel
from utils.colors import obtener_paleta, PALETAS
from utils.fonts import font_manager
from utils.images import img_manager
from utils.layouts import layout_engine
from config import PRESETS_TAMANO, TAMANO_OPCIONES

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
    return render_template("index.html", fuentes=fuentes, tamano_opciones=TAMANO_OPCIONES, paletas=PALETAS
                           , imagenes_agrupadas=img_manager.listar_agrupadas()
                           , overlays_agrupados=img_manager.listar_overlays_agrupadas())

@app.route("/generar", methods=["POST"])
def generar():
    texto = request.form["texto"]
    if not texto.strip():
        return {"ok": False, "error": "El texto no puede estar vacío"}, 400

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

    fondo_activar = request.form.get("fondo_activar")
    imagen_fondo_nombre = request.form.get("imagen_fondo", "") if fondo_activar else ""
    ruta_imagen_fondo = img_manager.obtener_ruta(imagen_fondo_nombre) if imagen_fondo_nombre else None
    opacidad_str = request.form.get("opacidad_imagen", "100")
    opacidad_imagen = int(opacidad_str) / 100.0

    overlay_activo = request.form.get("overlay_activo")
    colocaciones = None
    if overlay_activo:
        overlay_pack = request.form.get("overlay_pack", "placeholder")
        overlay_archivo = request.form.get("overlay_archivo", "circulo")
        overlay_posicion = request.form.get("overlay_posicion", "centro")
        overlay_tamano = int(request.form.get("overlay_tamano", 100))
        if overlay_pack == "placeholder":
            img_overlay = layout_engine.generar_placeholder(300, overlay_archivo)
        else:
            ruta_img = img_manager.obtener_ruta_overlay(overlay_pack, overlay_archivo)
            if ruta_img:
                img_overlay = Image.open(ruta_img).convert("RGBA")
            else:
                img_overlay = layout_engine.generar_placeholder(300, "circulo")
        modo = "detras" if overlay_posicion == "detras" else "imagen"
        params = {"posicion": overlay_posicion, "tamano_porcentaje": overlay_tamano}
        col = layout_engine.calcular_colocacion(modo, params, ancho, alto)
        col["imagen"] = img_overlay
        colocaciones = [col]

    plantilla = Carrusel(texto, color_fondo, color_texto, fuente=fuente,
                         num_slides=num_slides, tamano=tamano, alineacion=alineacion,
                         ancho=ancho, alto=alto, contorno_color=contorno_color,
                         contorno_grosor=contorno_grosor, sombra_offset=sombra_offset,
                         sombra_color=sombra_color, ruta_imagen_fondo=ruta_imagen_fondo,
                         opacidad_imagen=opacidad_imagen, colocaciones=colocaciones)

    imagenes = plantilla.render_all()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, img in enumerate(imagenes):
            img_buf = io.BytesIO()
            img.save(img_buf, format="PNG")
            zf.writestr(f"slide_{i+1:02d}.png", img_buf.getvalue())
    buf.seek(0)
    return send_file(buf, mimetype="application/zip", as_attachment=True,
                     download_name=f"contentforge_{timestamp}.zip")

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

    fondo_activar = request.form.get("fondo_activar")
    imagen_fondo_nombre = request.form.get("imagen_fondo", "") if fondo_activar else ""
    ruta_imagen_fondo = img_manager.obtener_ruta(imagen_fondo_nombre) if imagen_fondo_nombre else None
    opacidad_str = request.form.get("opacidad_imagen", "100")
    opacidad_imagen = int(opacidad_str) / 100.0

    slide_index = int(request.form.get("slide_index", 0))

    overlay_activo = request.form.get("overlay_activo")
    colocaciones = None
    if overlay_activo:
        overlay_pack = request.form.get("overlay_pack", "placeholder")
        overlay_archivo = request.form.get("overlay_archivo", "circulo")
        overlay_posicion = request.form.get("overlay_posicion", "centro")
        overlay_tamano = int(request.form.get("overlay_tamano", 100))
        if overlay_pack == "placeholder":
            img_overlay = layout_engine.generar_placeholder(300, overlay_archivo)
        else:
            ruta_img = img_manager.obtener_ruta_overlay(overlay_pack, overlay_archivo)
            if ruta_img:
                img_overlay = Image.open(ruta_img).convert("RGBA")
            else:
                img_overlay = layout_engine.generar_placeholder(300, "circulo")
        modo = "detras" if overlay_posicion == "detras" else "imagen"
        params = {"posicion": overlay_posicion, "tamano_porcentaje": overlay_tamano}
        col = layout_engine.calcular_colocacion(modo, params, ancho, alto)
        col["imagen"] = img_overlay
        colocaciones = [col]

    plantilla = Carrusel(
        texto, color_fondo, color_texto, fuente=fuente,
        num_slides=num_slides, tamano=tamano, alineacion=alineacion,
        ancho=ancho, alto=alto, contorno_color=contorno_color,
        contorno_grosor=contorno_grosor, sombra_offset=sombra_offset,
        sombra_color=sombra_color, ruta_imagen_fondo=ruta_imagen_fondo,
        opacidad_imagen=opacidad_imagen, colocaciones=colocaciones)
    img = plantilla.render_slide(slide_index)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    resp = send_file(buf, mimetype="image/png")
    resp.headers["X-Total-Slides"] = str(len(plantilla.textos))
    return resp


@app.route("/upload-fondo", methods=["POST"])
def upload_fondo():
    archivo = request.files.get("archivo")
    if not archivo or archivo.filename == "":
        return {"ok": False, "error": "No se envió ningún archivo"}, 400
    try:
        contenido = archivo.read()
        nombre = img_manager.guardar_archivo(archivo.filename, contenido)
        return {"ok": True, "nombre": nombre}
    except ValueError as e:
        return {"ok": False, "error": str(e)}, 400

@app.route("/listar-imagenes")
def listar_imagenes_json():
    img_manager.refrescar()
    return img_manager.listar_agrupadas()

if __name__ == "__main__":
    app.run(debug=True)