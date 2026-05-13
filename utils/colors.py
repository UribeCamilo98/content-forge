PALETAS = {
    "oscuro": {"fondo": (25, 25, 35), "texto": (255, 255, 255)},
    "claro": {"fondo": (245, 245, 245), "texto": (30, 30, 30)},
    "vibrante": {"fondo": (255, 65, 54), "texto": (255, 255, 255)},
    "naturaleza": {"fondo": (34, 139, 34), "texto": (255, 255, 255)},
    "pastel": {"fondo": (255, 182, 193), "texto": (80, 40, 60)},
    "neon": {"fondo": (0, 0, 0), "texto": (57, 255, 20)}
}

def obtener_paleta(nombre):
    if nombre in PALETAS:
        return PALETAS[nombre]
    else:
        return PALETAS["oscuro"]
    
    
