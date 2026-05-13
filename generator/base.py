from PIL import Image, ImageDraw
import os
from datetime import datetime

class PlantillaBase:
    def __init__(self, texto, color_fondo, color_texto):
        self.texto = texto
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def generar(self):
        from config import ANCHO, ALTO, MARGEN, RUTA_OUTPUT
        from utils.typography import ajustar_tamano_fuente, dividir_texto

        img = Image.new("RGB", (ANCHO, ALTO), self.color_fondo)
        draw = ImageDraw.Draw(img)

        lineas = dividir_texto(self.texto)
        linea_mas_larga =max(lineas, key=len)

        ancho_disponible = ANCHO - (MARGEN*2)
        tamano_fuente, fuente = ajustar_tamano_fuente(linea_mas_larga, ancho_disponible)

        alto_total = len(lineas) * tamano_fuente
        y_inicial = (ALTO - alto_total) // 2
    
        for i, linea in enumerate(lineas):
            bbox = draw.textbbox((0, 0), linea, font=fuente)
            ancho_linea = bbox[2] - bbox[0]
            x = (ANCHO - ancho_linea) // 2
            y = y_inicial + i * tamano_fuente
            draw.text((x, y), linea, font=fuente, fill=self.color_texto)
    
        os.makedirs(RUTA_OUTPUT, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = os.path.join(RUTA_OUTPUT, f"imagen_{timestamp}.png")
        img.save(ruta)
        return ruta



