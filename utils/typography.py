from PIL import ImageFont, ImageDraw, Image

def ajustar_tamano_fuente(texto, ancho_maximo, tamano_inicial=80, ruta_fuente = None):
    if ruta_fuente is None:
        ruta_fuente = "C:/Windows/Fonts/arial.ttf"
    tamano = tamano_inicial
    img_temp = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(img_temp)
    while True:
        fuente = ImageFont.truetype(ruta_fuente, tamano)
        bbox = draw.textbbox((0, 0), texto, font=fuente)
        ancho_texto = bbox[2] - bbox[0]
        if ancho_texto <= ancho_maximo:
            break
        tamano -= 2
    return tamano, fuente

def dividir_texto(texto, max_lineas=5):
    palabras = texto.split()
    if max_lineas <= 1 or len(palabras) <= 1:
        return [texto]

    num_lineas = min(max_lineas, len(palabras))
    palabras_por_linea = (len(palabras) + num_lineas - 1) // num_lineas
    lineas = []
    for i in range(0, len(palabras), palabras_por_linea):
        grupo = palabras[i:i + palabras_por_linea]
        lineas.append(" ".join(grupo))
    return lineas