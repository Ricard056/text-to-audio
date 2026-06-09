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
- `main.py`              — toda la lógica. Config arriba (incl. `EDGE_VOICE_*`, `LANGUAGE_MAP`) + clase `TextToAudioConverter`.
- `setup.py`             — instala dependencias y crea carpetas.
- `run.bat` / `run_offline.bat` — ejecutar modo normal (edge) / forzado offline. Ver `TTS_ENGINE`.
- `list_voices.py` / `list_voices.bat` — listan voces offline SAPI5 + recordatorio de comandos edge.
- `export_edge_voices.bat` — vuelca voces edge a `docs/voices_en-US.md` y `docs/voices_es.md`.
- `docs/`               — listas de voces de referencia (versionado).
- `voice_tests_input/`  — textos de ejemplo por estilo de voz (versionado, **NO** se procesa solo).
- `input/`              — entrada. **El sufijo del nombre define el idioma** (`_en`, `_mx`, `_es`).
- `output/`             — audio generado (ignorado por git).
- `output__resp_local/` — audios que el usuario quiera conservar (ignorado por git).
- `requirements.txt`, `README.md`, `USAGE_TESTING.md`, `audio_notes.md`.

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
- **Routing de idioma:** `LANGUAGE_MAP` (en `main.py`) controla sufijos→locale y la voz por
  backend (`suffixes`, `edge_voice`, `offline_match`). `detect_language(stem)` lo usa.
- **Cambiar voces edge (forma recomendada):** editar las constantes `EDGE_VOICE_EN` /
  `EDGE_VOICE_MX` / `EDGE_VOICE_ES` arriba en `main.py`; `LANGUAGE_MAP` las referencia. No hace
  falta editar el dict directamente.
- **Motor:** `ENGINE = os.getenv("TTS_ENGINE", "edge")` → `edge` (MP3) u `offline` (WAV);
  valor desconocido → `offline` con aviso. `run_offline.bat` exporta `TTS_ENGINE=offline`.
- offline: primera voz SAPI5 cuyo nombre/id matchee `offline_match` (términos por prioridad).
- Listar voces: `edge-tts --list-voices` (online), `list_voices.py/.bat` (offline),
  `export_edge_voices.bat` (volcado a `docs/`).

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
- `setup.py` escribe un `input/test_en.txt` de prueba (sufijo `_en` → voz inglesa).

## No cambiar salvo que se pida explícitamente (Do not change unless requested)
- **No** mover la configuración a JSON / `config.py`: las voces viven en constantes
  `EDGE_VOICE_*` dentro de `main.py` a propósito (menor riesgo, con comentarios).
- **No** implementar una CLI completa (solo existe la env var `TTS_ENGINE`).
- **No** implementar chunking, caché ni normalización de texto sin que el usuario lo pida.
- **No** cambiar el flujo principal `input/` → `output/` (glob de `input/`, extensión = formato real).

## Mejoras futuras (opcionales, no implementadas — requieren petición explícita)
- Normalización de texto, división de frases.
- CLI args para sobreescribir config.
- Caché de audio por hash de texto+voz.
- Autodetección de idioma como fallback del sufijo.
