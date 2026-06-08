# CLAUDE.md — Text to Audio Converter

Mapa del proyecto para futuras sesiones de Claude Code. Breve a propósito.

## Propósito
Convertir archivos TXT/PDF/DOCX a audio con TTS. Proyecto personal, simple.

## Cómo correrlo
- Setup único: `python setup.py` (instala deps, crea carpetas).
- Uso: poner archivos en `input/`, correr `python main.py`, recoger audio en `output/`.
- Windows: `run.bat` (modo normal) y `run_offline.bat` (fuerza offline) por doble clic.
- Motor: `ENGINE` se lee de la env var `TTS_ENGINE` (`edge` por defecto / `offline`); valor
  desconocido cae a `offline` con aviso. Config restante: constantes al inicio de `main.py` (no hay CLI).

## Estructura
- `main.py`         — toda la lógica. Config arriba + clase `TextToAudioConverter`.
- `setup.py`        — instala dependencias y crea carpetas.
- `input/`          — entrada. **El sufijo del nombre define el idioma** (`_en`, `_mx`, `_es`).
- `output/`         — audio generado (ignorado por git).
- `requirements.txt`, `README.md`, `audio_notes.md`.

## Flujo texto → audio
`run()` → glob de `input/` → `read_file()` (txt/pdf/docx) → `text_to_audio(text, stem)`:
1. `detect_language(stem)` → locale por sufijo (`LANGUAGE_MAP`), o `DEFAULT_LANGUAGE`.
2. Si `ENGINE="edge"`: `synthesize_edge()` → MP3 neural. Si falla, cae a offline.
3. `synthesize_offline()` → pyttsx3/SAPI5 → WAV (engine nuevo por archivo).
La extensión SIEMPRE refleja el formato real (mp3 = edge, wav = offline).

## Dependencias
- `edge-tts` — voces neurales, MP3 real, gratis, sin API key, **requiere internet**.
- `pyttsx3` — voces SAPI5 locales de Windows, WAV, offline (fallback).
- `PyPDF2`, `python-docx` — extracción de texto.

## Idiomas y voces
- Idioma por sufijo de archivo (ver `LANGUAGE_MAP` en `main.py`).
- edge: `en-US-AriaNeural`, `es-MX-DaliaNeural`, `es-ES-ElviraNeural` (cambiables).
- offline: primera voz SAPI5 cuyo nombre/id haga match de `offline_match`.
- Listar voces edge: `edge-tts --list-voices`.

## Problemas conocidos / decisiones
- **Causa histórica del "inglés malo":** antes la voz era global y en español; ahora se elige
  por archivo según el idioma. Resuelto.
- Las voces neurales de Win11 NO son accesibles vía pyttsx3 (por eso edge-tts es el backend
  principal de calidad).
- pyttsx3/SAPI5 no produce MP3 ni soporta SSML de forma fiable → backend offline emite WAV.
- edge-tts necesita internet; sin red se usa automáticamente el backend offline.

## Áreas frágiles
- Extracción de PDFs complejos (PyPDF2 puede devolver texto pobre).
- Encoding de TXT: se intentan utf-8 / utf-8-sig / cp1252 / latin-1.
- `setup.py` aún escribe un `input/test.txt` de prueba (sin sufijo → DEFAULT_LANGUAGE).

## Mejoras futuras (opcionales, no implementadas)
- Normalización de texto, división de frases.
- CLI args para sobreescribir config.
- Caché de audio por hash de texto+voz.
- Autodetección de idioma como fallback del sufijo.
