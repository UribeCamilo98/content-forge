PALETAS = {
    "oscuro": {"fondo": (25, 25, 35), "texto": (255, 255, 255)},
    "claro": {"fondo": (245, 245, 245), "texto": (30, 30, 30)},
    "naturaleza": {"fondo": (34, 139, 34), "texto": (255, 255, 255)},
    "pastel": {"fondo": (255, 182, 193), "texto": (80, 40, 60)},
    "neon": {"fondo": (0, 0, 0), "texto": (57, 255, 20)},
    "sabrina":{"fondo":(242, 233, 216), "texto":(140, 92, 50)},
    "violeta":{"fondo":(36, 41, 76), "texto":(155, 147, 250)}
}

def obtener_paleta(nombre):
    if nombre in PALETAS:
        return PALETAS[nombre]
    else:
        return PALETAS["oscuro"]
    
    
