# content‑forge

Aplicación web local para generar imágenes estáticas para TikTok (carruseles, frases, anuncios) usando Python + Flask + Pillow.

## Características (v1.1)

- **Carrusel de N slides** — divide automáticamente el texto en slides (por oraciones y párrafos)
- **Fuentes externas** — selector de fuentes .ttf con auto-ajuste si el texto no cabe
- **Tamaño de fuente manual** — slider de 10 a 200 px
- **Alineación de texto** — izquierda, centro, derecha
- **Borde y sombra en texto** — contorno configurable (color + grosor) y sombra desplazada (offset X/Y + color)
- **Selector de color interactivo** — color pickers hex + paletas predefinidas sincronizadas
- **Preview en vivo (AJAX)** — vista previa automática sin recargar la página, con navegación entre slides
- **Presets de tamaño** — cuadrado (1080×1080), vertical (1080×1920), horizontal (1920×1080)
- **Paletas de color** — varios esquemas predefinidos
- **Salida organizada** — cada generación crea `output/YYYYMMDD_HHMMSS/` con `slide_01.png`, etc.

> ⚠️ La alineación "justificado" está presente en la interfaz pero aún no implementada (se comporta como centro).

## Requisitos

- Python 3.9+
- pip

## Instalación

```bash
git clone <repo>
cd contentforge
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Abrir `http://localhost:5000`. Escribir texto, elegir opciones, ver el preview en vivo y hacer clic en "Generar Carrusel".

## Tests

```bash
pytest tests/ -v
```

## Roadmap

| Versión | Estado      |
|---------|-------------|
| v1.0    | ✅ Completa |
| v1.1    | ✅ Completa |
| v1.2    | 🔜 Imágenes de fondo |
| v1.3    | 🔮 Layouts con imágenes |
| v1.4    | 🔮 Editor visual con canvas |
