# content‑forge

Aplicación web local para generar imágenes estáticas para TikTok (carruseles, frases, anuncios) usando Python + Flask + Pillow.

## Características (v1.0)

- **Carrusel de N slides** — divide automáticamente el texto en slides (por oraciones y párrafos)
- **Fuentes externas** — selector de fuentes .ttf con auto-ajuste si el texto no cabe
- **Tamaño de fuente manual** — slider de 10 a 200 px
- **Alineación de texto** — izquierda, centro, derecha y justificado
- **Presets de tamaño** — cuadrado (1080×1080), vertical (1080×1920), horizontal (1920×1080)
- **Paletas de color** — varios esquemas predefinidos
- **Salida organizada** — cada generación crea `output/YYYYMMDD_HHMMSS/` con `slide_01.png`, etc.

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

Abrir `http://localhost:5000`. Escribir texto, elegir opciones y hacer clic en "Generar".

## Tests

```bash
pytest tests/ -v
```

## Roadmap

| Versión | Estado      |
|---------|-------------|
| v1.0    | ✅ Completa |
| v1.1    | 🔜 Imágenes de fondo + layouts |
| v1.2    | 🔮 Editor visual con canvas |
