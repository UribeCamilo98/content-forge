import math
from PIL import Image, ImageDraw

class LayoutEngine:
    FORMAS_PLACEHOLDER = ["circulo", "estrella", "cuadrado"]

    @staticmethod
    def generar_placeholder(tamano, forma="circulo", color=None):
        img = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        if color is None:
            color = (90, 170, 220)
        color_con_alpha = (*color, 255)
        margen = 2
        if forma == "circulo":
            draw.ellipse(
                [margen, margen, tamano - margen, tamano - margen],
                fill=color_con_alpha
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
            draw.polygon(pts, fill=color_con_alpha)
        elif forma == "cuadrado":
            draw.rectangle(
                [margen, margen, tamano - margen, tamano - margen],
                fill=color_con_alpha
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

    @staticmethod
    def calcular_colocaciones(modo, params, ancho_slide, alto_slide):
        import random
        if modo == "collage":
            cantidad = int(params.get("cantidad", 5))
            tam_min = float(params.get("tam_min", 30)) / 100.0
            tam_max = float(params.get("tam_max", 100)) / 100.0
            area = params.get("area", "alrededor")
            separacion = float(params.get("separacion", 50)) / 100.0
            factor = math.sqrt(separacion)
            rotacion_aleatoria = params.get("rotacion_aleatoria", False)

            lado_base = min(ancho_slide, alto_slide)

            if area == "alrededor":
                cx = ancho_slide // 2
                cy = alto_slide // 2
                max_r = min(ancho_slide, alto_slide) * 0.4

                colocaciones = []
                for i in range(cantidad):
                    t = i / (cantidad - 1) if cantidad > 1 else 0
                    angle = i / cantidad * 2 * math.pi
                    radius = int(max_r * factor * t)

                    pct = tam_min + t * (tam_max - tam_min)
                    lado = int(lado_base * pct * 0.7)
                    lado = max(20, lado)

                    x = int(cx + radius * math.cos(angle)) - lado // 2
                    y = int(cy + radius * math.sin(angle)) - lado // 2

                    colocaciones.append({"x": x, "y": y, "w": lado, "h": lado})

            else:
                if area in ("izquierda", "derecha"):
                    prim_min, prim_max = 0, alto_slide
                    sec_max = ancho_slide
                    sec_base = 0 if area == "izquierda" else ancho_slide
                else:
                    prim_min, prim_max = 0, ancho_slide
                    sec_max = alto_slide
                    sec_base = 0 if area == "arriba" else alto_slide

                sec_sign = 1 if area in ("izquierda", "arriba") else -1
                prim_center = (prim_min + prim_max) // 2
                prim_span = prim_max - prim_min

                colocaciones = []
                for i in range(cantidad):
                    t_sec = i / (cantidad - 1) if cantidad > 1 else 0
                    sec_offset = int(t_sec * sec_max * factor)
                    sec_pos = sec_base + sec_sign * sec_offset

                    pct = tam_max - t_sec * (tam_max - tam_min)
                    lado = int(lado_base * pct * 0.7)
                    lado = max(20, lado)

                    t_prim = i / (cantidad - 1) if cantidad > 1 else 0.5
                    t_scaled = 0.5 + (t_prim - 0.5) * factor
                    prim_pos = int(prim_min + t_scaled * prim_span)
                    prim_pos = max(prim_min + lado // 2, min(prim_pos, prim_max - lado // 2))

                    if area in ("izquierda", "derecha"):
                        x = sec_pos - lado // 2
                        y = prim_pos - lado // 2
                    else:
                        x = prim_pos - lado // 2
                        y = sec_pos - lado // 2

                    colocaciones.append({"x": x, "y": y, "w": lado, "h": lado})

            if rotacion_aleatoria:
                for col in colocaciones:
                    col["rotacion"] = random.randint(0, 360)
            return colocaciones

        if modo == "tapiz":
            direccion = params.get("direccion", "horizontal")
            tam_celda = int(params.get("tam_celda", 150))
            espaciado = int(params.get("espaciado", 10))
            step = tam_celda + espaciado
            lado_base = min(ancho_slide, alto_slide)
            lado = min(tam_celda, lado_base)
            colocaciones = []

            if direccion == "horizontal":
                for x in range(0, ancho_slide + step, step):
                    col = {"x": x - lado // 2, "y": alto_slide // 2 - lado // 2, "w": lado, "h": lado}
                    colocaciones.append(col)
            elif direccion == "vertical":
                for y in range(0, alto_slide + step, step):
                    col = {"x": ancho_slide // 2 - lado // 2, "y": y - lado // 2, "w": lado, "h": lado}
                    colocaciones.append(col)
            elif direccion == "diagonal":
                max_dim = max(ancho_slide, alto_slide)
                for i in range(0, max_dim + step, step):
                    col = {"x": i - lado // 2, "y": i - lado // 2, "w": lado, "h": lado}
                    colocaciones.append(col)
            return colocaciones

        return []

layout_engine = LayoutEngine()
