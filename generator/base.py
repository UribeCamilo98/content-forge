from PIL import Image, ImageDraw
from config import PRESETS_TAMANO, MARGEN
from utils.typography import ajustar_tamano_fuente, dividir_texto
from utils.fonts import font_manager

class PlantillaBase:
    def __init__(self, color_fondo, color_texto):
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def _crear_imagen(self, texto, fuente = None, tamano = None, alineacion = "centro", ancho=None, 
                      alto=None, contorno_color=None, contorno_grosor=3, sombra_offset=None, sombra_color=(128, 128, 128)):
        if ancho == None and alto == None:
            ancho,alto = PRESETS_TAMANO["cuadrado"]
        img = Image.new("RGB", (ancho, alto), self.color_fondo)
        draw = ImageDraw.Draw(img)

        lineas = dividir_texto(texto)
        linea_mas_larga = max(lineas, key=len)
        ancho_disponible = ancho - MARGEN*2

        if fuente and fuente in font_manager.listar_fuentes():
            ruta_fuente = font_manager.obtener_ruta(fuente)
        else:
            ruta_fuente = "C:/Windows/Fonts/arial.ttf"

        if tamano:
            from PIL import ImageFont
            tamano_fuente = tamano
            while True:
                fuente_pil = ImageFont.truetype(ruta_fuente, tamano_fuente)
                bbox = draw.textbbox((0, 0), linea_mas_larga, font=fuente_pil)
                ancho_necesario = bbox[2] - bbox[0]
                alto_necesario = len(lineas) * tamano_fuente
                if ancho_necesario <= ancho_disponible and alto_necesario <= alto:
                    break
                tamano_fuente -= 2
                if tamano_fuente < 12:
                    break
        else:
            tamano_fuente, fuente_pil = ajustar_tamano_fuente(
                linea_mas_larga, ancho_disponible, ruta_fuente = ruta_fuente
            )


        alto_total = len(lineas) * tamano_fuente
        y_inicial = (alto - alto_total)//2

        for i, linea in enumerate(lineas):
            bbox= draw.textbbox((0, 0), linea, font=fuente_pil)
            ancho_linea = bbox[2] - bbox[0]
            
            if alineacion == "izquierda":
                x = MARGEN
            elif alineacion == "derecha":
                x = ancho - MARGEN - ancho_linea
            else:
                x = (ancho - ancho_linea) // 2

            y = y_inicial + i * tamano_fuente

            if sombra_offset:
                sx, sy= sombra_offset
                draw.text((x + sx, y + sy), linea, font=fuente_pil, fill=sombra_color)

            if contorno_color:
                for dx, dy in [(-1,-1), (0,-1), (1,-1),
                           (-1,0), (1,0),
                           (-1,1), (0,1), (1,1)]:
                    draw.text((x + dx * contorno_grosor, y + dy * contorno_grosor), linea, font=fuente_pil, fill=contorno_color)

            draw.text((x,y), linea, font=fuente_pil, fill=self.color_texto)
        
        return img
    

