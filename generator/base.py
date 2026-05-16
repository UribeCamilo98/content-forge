from PIL import Image, ImageDraw
from config import ANCHO, ALTO, MARGEN
from utils.typography import ajustar_tamano_fuente, dividir_texto

class PlantillaBase:
    def __init__(self, color_fondo, color_texto):
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def _crear_imagen(self, texto):
        img = Image.new("RGB", (ANCHO, ALTO), self.color_fondo)
        draw = ImageDraw.Draw(img)

        lineas = dividir_texto(texto)
        linea_mas_larga = max(lineas, key=len)
        ancho_disponible = ANCHO - MARGEN*2
        tamano_fuente, fuente = ajustar_tamano_fuente(linea_mas_larga, ancho_disponible)

        alto_total = len(lineas) * tamano_fuente
        y_inicial = (ALTO - alto_total)//2

        for i, linea in enumerate(lineas):
            bbox= draw.textbbox((0, 0), linea, font=fuente)
            ancho_linea = bbox[2] - bbox[0]
            x = (ANCHO - ancho_linea) // 2
            y = y_inicial + i * tamano_fuente
            draw.text((x,y), linea, font=fuente, fill=self.color_texto)
        
        return img

