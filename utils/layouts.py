import math
import random
from PIL import Image, ImageDraw

class LayoutEngine:
    FORMAS_PLACEHOLDER = ["circulo", "estrella", "diamante", "marco"]

    @staticmethod
    def generar_placeholder(tamano, forma="circulo"):
        img = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
            200
        )
        margen = 2
        if forma == "circulo":
            draw.ellipse(
                [margen, margen, tamano - margen, tamano - margen],
                fill=color
            )
        elif forma == "estrella":
            cx = cy = tamano // 2
            r_ext = tamano // 2 - margen
            r_int = r_ext // 2
            pts = []
            for i in range(10):
                ang = math.pi / 2 + i * math.pi / 5
                r = r_ext if i % 2 == 0 else r_int
                pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
            draw.polygon(pts, fill=color)
        elif forma == "diamante":
            draw.polygon([
                (tamano // 2, margen),
                (tamano - margen, tamano // 2),
                (tamano // 2, tamano - margen),
                (margen, tamano // 2)
            ], fill=color)
        elif forma == "marco":
            grosor = max(4, tamano // 10)
            draw.rectangle(
                [margen, margen, tamano - margen, tamano - margen],
                outline=color, width=grosor
            )
            draw.rectangle(
                [margen, margen, tamano - margen, tamano - margen],
                fill=(*color[:3], 60)
            )
        return img

    @staticmethod
    def calcular_colocacion(modo, params, ancho_slide, alto_slide):
        pct = float(params.get("tamano_porcentaje", 100)) / 100.0
        posicion = params.get("posicion", "centro")
        lado_base = min(ancho_slide, alto_slide)
        lado = int(lado_base * pct * 0.7)
        w = lado
        h = lado
        if modo == "detras":
            lado = max(ancho_slide, alto_slide) * pct
            w = int(lado)
            h = int(lado)
            x = (ancho_slide - w) // 2
            y = (alto_slide - h) // 2
        elif posicion == "centro":
            x = (ancho_slide - w) // 2
            y = (alto_slide - h) // 2
        elif posicion == "izquierda":
            x = -w // 4
            y = (alto_slide - h) // 2
        elif posicion == "derecha":
            x = ancho_slide - w * 3 // 4
            y = (alto_slide - h) // 2
        elif posicion == "arriba":
            x = (ancho_slide - w) // 2
            y = -h // 4
        elif posicion == "abajo":
            x = (ancho_slide - w) // 2
            y = alto_slide - h * 3 // 4
        else:
            x = (ancho_slide - w) // 2
            y = (alto_slide - h) // 2
        return {"x": x, "y": y, "w": w, "h": h}

layout_engine = LayoutEngine()
