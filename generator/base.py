from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from config import PRESETS_TAMANO, MARGEN, TEXTO_AREA
from utils.typography import dividir_texto
from utils.fonts import font_manager

class PlantillaBase:
    def __init__(self, color_fondo, color_texto):
        self.color_fondo = color_fondo
        self.color_texto = color_texto

    def _componer_imagenes(self, fondo, colocaciones):
        if fondo.mode != "RGBA":
            fondo = fondo.convert("RGBA")
        for col in colocaciones:
            img_overlay = col["imagen"]
            w, h = col["w"], col["h"]
            img_redim = img_overlay.resize((w, h), Image.LANCZOS)
            if img_redim.mode != "RGBA":
                img_redim = img_redim.convert("RGBA")

            flip_x = col.get("flip_x", False)
            flip_y = col.get("flip_y", False)
            rotacion = col.get("rotacion", 0)
            opacidad = col.get("opacidad", 1.0)
            borde_color = col.get("borde_color")
            borde_grosor = col.get("borde_grosor", 2)
            sombra_offset = col.get("sombra_offset")
            sombra_color = col.get("sombra_color")

            if flip_x:
                img_redim = img_redim.transpose(Image.FLIP_LEFT_RIGHT)
            if flip_y:
                img_redim = img_redim.transpose(Image.FLIP_TOP_BOTTOM)

            paste_x, paste_y = col["x"], col["y"]
            if rotacion:
                cx = paste_x + img_redim.width // 2
                cy = paste_y + img_redim.height // 2
                img_redim = img_redim.rotate(rotacion, expand=True, fillcolor=(0, 0, 0, 0))
                paste_x = cx - img_redim.width // 2
                paste_y = cy - img_redim.height // 2

            if opacidad < 1.0:
                alpha = img_redim.split()[3]
                alpha = alpha.point(lambda a: int(a * opacidad))
                img_redim.putalpha(alpha)

            if sombra_offset and sombra_color:
                sx, sy = sombra_offset
                r, g, b, a = img_redim.split()
                sombra_img = Image.new("RGBA", img_redim.size, (*sombra_color, 0))
                sombra_img.putalpha(a)
                alpha_borroso = sombra_img.split()[3].filter(
                    ImageFilter.GaussianBlur(radius=4)
                )
                sombra_img.putalpha(alpha_borroso)
                alpha_s = sombra_img.split()[3]
                alpha_s = alpha_s.point(lambda v: int(v * 0.6))
                sombra_img.putalpha(alpha_s)
                capa_s = Image.new("RGBA", fondo.size, (0, 0, 0, 0))
                capa_s.paste(sombra_img, (paste_x + sx, paste_y + sy))
                fondo = Image.alpha_composite(fondo, capa_s)

            if borde_color:
                a = img_redim.split()[3]
                kernel = borde_grosor * 2 + 1
                a_dil = a.filter(ImageFilter.MaxFilter(kernel))
                outline = ImageChops.subtract(a_dil, a)
                borde_layer = Image.new("RGBA", img_redim.size, (*borde_color, 255))
                borde_layer.putalpha(outline)
                img_redim = Image.alpha_composite(borde_layer, img_redim)

            capa = Image.new("RGBA", fondo.size, (0, 0, 0, 0))
            capa.paste(img_redim, (paste_x, paste_y))
            fondo = Image.alpha_composite(fondo, capa)
        return fondo

    def _crear_imagen(self, texto, fuente = None, tamano = None, alineacion = "centro", ancho=None, 
                      alto=None, contorno_color=None, contorno_grosor=3, sombra_offset=None, sombra_color=(128, 128, 128),
                      ruta_imagen_fondo = None, opacidad_imagen=1.0, colocaciones=None):
        if ancho is None and alto is None:
            ancho,alto = PRESETS_TAMANO["cuadrado"]
        if ruta_imagen_fondo:
            img = Image.open(ruta_imagen_fondo).convert("RGB")
            img = img.resize((ancho,alto), Image.LANCZOS)
            if opacidad_imagen < 1.0:
                color_solido = Image.new("RGB", (ancho, alto), self.color_fondo)
                img = Image.blend(color_solido, img, opacidad_imagen)
        else:
            img = Image.new("RGB", (ancho, alto), self.color_fondo)
        if colocaciones:
            img = self._componer_imagenes(img, colocaciones)
        draw = ImageDraw.Draw(img)

        offset_x = (ancho - TEXTO_AREA) //2
        offset_y = (alto - TEXTO_AREA) //2
        ancho_disponible = TEXTO_AREA - MARGEN*2

        if fuente and fuente in font_manager.listar_fuentes():
            ruta_fuente = font_manager.obtener_ruta(fuente)
        else:
            ruta_fuente = "C:/Windows/Fonts/arial.ttf"

        palabras = texto.split()
        len_palabras = max(len(palabras), 1)
        tamano_inicial = tamano if tamano else 80
        tamano_fuente = tamano_inicial
        
        
        while True:
            target_lines = max(2, min(len_palabras, int(TEXTO_AREA * 0.75 / tamano_fuente)))
            lineas = dividir_texto(texto,max_lineas=target_lines)
            linea_mas_larga = max(lineas, key=len)
            fuente_pil = ImageFont.truetype(ruta_fuente, tamano_fuente)
            bbox = draw.textbbox((0, 0), linea_mas_larga, font=fuente_pil)
            ancho_necesario = bbox[2] - bbox[0]
            alto_necesario = len(lineas) * tamano_fuente
            if ancho_necesario <= ancho_disponible and alto_necesario <= TEXTO_AREA:
                break
            tamano_fuente -= 2
            if tamano_fuente < 12:
                break
    


        alto_total = len(lineas) * tamano_fuente
        y_inicial = offset_y + (TEXTO_AREA - alto_total) // 2

        for i, linea in enumerate(lineas):
            y = y_inicial + i * tamano_fuente
            fragmentos = []

            if alineacion == "justificado":
                palabras_linea = linea.split()
                if len(palabras_linea) <= 1:
                    bbox = draw.textbbox((0, 0), linea, font=fuente_pil)
                    ancho_linea = bbox[2] - bbox[0]
                    x = offset_x + (TEXTO_AREA - ancho_linea) // 2
                    fragmentos.append((linea, x, y))
                else:
                    palabras_bbox = [draw.textbbox((0, 0), p, font=fuente_pil) for p in palabras_linea]
                    ancho_palabras = sum(b[2] - b[0] for b in palabras_bbox)
                    espacio_extra = (ancho_disponible - ancho_palabras) / (len(palabras_linea) - 1)
                    x = offset_x + MARGEN
                    for idx, palabra in enumerate(palabras_linea):
                        ap = palabras_bbox[idx][2] - palabras_bbox[idx][0]
                        fragmentos.append((palabra, x, y))
                        if idx < len(palabras_linea) - 1:
                            x += ap + espacio_extra
            else:
                bbox = draw.textbbox((0, 0), linea, font=fuente_pil)
                ancho_linea = bbox[2] - bbox[0]
                if alineacion == "izquierda":
                    x = offset_x + MARGEN
                elif alineacion == "derecha":
                    x = offset_x + TEXTO_AREA - MARGEN - ancho_linea
                else:
                    x = offset_x + (TEXTO_AREA - ancho_linea) // 2
                fragmentos.append((linea, x, y))

            for texto_frag, x_frag, y_frag in fragmentos:
                if sombra_offset:
                    sx, sy = sombra_offset
                    draw.text((x_frag + sx, y_frag + sy), texto_frag, font=fuente_pil, fill=sombra_color)
                if contorno_color:
                    for dx, dy in [(-1, -1), (0, -1), (1, -1),
                                   (-1, 0), (1, 0),
                                   (-1, 1), (0, 1), (1, 1)]:
                        draw.text((x_frag + dx * contorno_grosor, y_frag + dy * contorno_grosor),
                                  texto_frag, font=fuente_pil, fill=contorno_color)
                draw.text((x_frag, y_frag), texto_frag, font=fuente_pil, fill=self.color_texto)
        
        return img
    

