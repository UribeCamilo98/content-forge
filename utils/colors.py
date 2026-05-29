PALETAS = {
    "oscuro": {"fondo": "#191923", "texto": "#ffffff"},
    "claro": {"fondo": "#f5f5f5", "texto": "#1e1e1e"},
    "naturaleza": {"fondo": "#228b22", "texto": "#ffffff"},
    "pastel": {"fondo": "#ffb6c1", "texto": "#50283c"},
    "neon": {"fondo": "#000000", "texto": "#39ff14"},
    "sabrina":{"fondo":"#f2e9d8", "texto":"#8c5c32"},
    "violeta":{"fondo":"#24294c", "texto":"#9b93fa"}
}

def obtener_paleta(nombre):
    if nombre in PALETAS:
        return PALETAS[nombre]
    else:
        return PALETAS["oscuro"]
    
    
