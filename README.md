# Text to Audio Converter

Convierte archivos TXT, PDF y DOCX a audio. Elige idioma y voz **por archivo** según el sufijo
del nombre, y usa voces neurales de alta calidad cuando hay internet.

## Cómo funciona (resumen)

- **Backend `edge`** (por defecto): voces neurales vía `edge-tts`. Gratis, sin API key,
  **requiere internet**. Genera **MP3 real**.
- **Backend `offline`**: voces SAPI5 de Windows vía `pyttsx3`. Funciona sin internet.
  Genera **WAV real**. Se usa también como *fallback* automático si edge-tts falla.

> Nota: las voces neurales modernas de Windows 11 no son accesibles desde `pyttsx3`; por eso
> la mejor calidad viene de `edge-tts`. La salida nunca es un WAV disfrazado de `.mp3`: la
> extensión siempre refleja el formato real.

## Quick Start

### 1. Setup (una vez)
```bash
python setup.py        # instala dependencias y crea carpetas
# o manualmente:
pip install -r requirements.txt
```

### 2. Agrega tus archivos
Coloca `.txt`, `.pdf` o `.docx` en la carpeta `input/`.

**El sufijo del nombre define el idioma:**

| Sufijo            | Idioma            | Ejemplo            |
|-------------------|-------------------|--------------------|
| `_en`             | Inglés (en-US)    | `report_en.txt`    |
| `_mx`             | Español México    | `nota_mx.txt`      |
| `_es`             | Español España    | `carta_es.txt`     |
| (sin sufijo)      | `DEFAULT_LANGUAGE`| `apuntes.txt`      |

### 3. Ejecuta
```bash
python main.py
```

En Windows puedes usar los accesos directos (doble clic):
- **`run.bat`** — modo normal (edge-tts, MP3, con fallback automático a offline).
- **`run_offline.bat`** — fuerza el modo offline (pyttsx3/SAPI5, WAV, sin internet).

También puedes forzar el motor con la variable de entorno `TTS_ENGINE` (`edge` u `offline`),
sin editar el código. Ej.: `set TTS_ENGINE=offline` antes de `python main.py`.

### 4. Recoge el audio
En `output/`: `.mp3` si se usó edge-tts, `.wav` si se usó el backend offline.

¿Quieres **conservar** algún audio (por ejemplo para comparar voces)? Muévelo a
`output__resp_local/`. Esa carpeta es tu archivo personal y **no se versiona** en git, así que
puedes guardar ahí lo que quieras sin ensuciar el repositorio.

## Configuración

Edita las constantes al inicio de `main.py`:

```python
ENGINE = "edge"            # "edge" (neural, MP3, internet) o "offline" (SAPI5, WAV)
DEFAULT_LANGUAGE = "es-MX" # idioma para archivos sin sufijo reconocido
SPEECH_RATE = 150          # solo backend offline: 100=lento, 150=normal, 200=rápido
VOLUME = 1.0               # solo backend offline: 0.0 a 1.0
```

### Cambiar voces

Para cambiar la voz edge de cada idioma, edita estas constantes cerca del inicio de `main.py`
(no hace falta tocar `LANGUAGE_MAP`):
```python
EDGE_VOICE_EN = "en-US-AriaNeural"    # Inglés         - femenina
EDGE_VOICE_MX = "es-MX-DaliaNeural"   # Español México - femenina
EDGE_VOICE_ES = "es-ES-ElviraNeural"  # Español España - femenina
```
Ejemplo voz masculina en inglés: `EDGE_VOICE_EN = "en-US-GuyNeural"`.

Ver voces disponibles:
```bash
edge-tts --list-voices                 # voces online (edge)
edge-tts --list-voices | findstr en-US # filtrar por idioma (Windows)
```
- **`list_voices.bat`** (doble clic) — lista las voces **offline** (SAPI5) instaladas en tu
  Windows y recuerda los comandos de edge. (Equivale a `python list_voices.py`.)
- **`export_edge_voices.bat`** (doble clic) — guarda una **referencia local** de las voces
  **online** en `docs/voices_en-US.md` y `docs/voices_es.md`, con la fecha de generación.

¿Quieres comparar varias voces con el mismo texto? En `voice_tests_input/` hay textos de
ejemplo en inglés (uno por estilo de voz). Copia uno a `input/`, cambia `EDGE_VOICE_EN` y corre
`run.bat`. Esa carpeta **no se procesa sola**; solo se usa lo que copies a `input/`.

## Estructura
```
20250816_text_to_audio/
├── main.py                 # lógica + configuración (incl. EDGE_VOICE_*)
├── setup.py                # instala dependencias y crea carpetas
├── requirements.txt
├── run.bat                 # ejecutar en modo normal (edge)
├── run_offline.bat         # ejecutar forzando offline (SAPI5)
├── list_voices.py / .bat   # listar voces offline
├── export_edge_voices.bat  # guardar referencia de voces edge en docs/
├── README.md               # esta guía
├── USAGE_TESTING.md        # guía de prueba/verificación
├── CLAUDE.md               # mapa técnico del proyecto
├── audio_notes.md
├── docs/                   # listas de voces de referencia (versionado)
├── voice_tests_input/      # textos de ejemplo por estilo (versionado, NO se procesa solo)
├── input/                  # tus archivos (sufijo = idioma)
├── output/                 # audio generado (NO versionado)
└── output__resp_local/     # audios que quieras conservar (NO versionado)
```

### Qué se versiona y qué no
- **Sí** se versiona: el código, los `.bat`, la documentación, `docs/` y `voice_tests_input/`.
- **No** se versiona (git lo ignora): `output/`, `output__resp_local/`, `input/` y las carpetas
  de trabajo local. Ahí van tus archivos personales y los audios generados.

## Troubleshooting

- **El inglés sonaba mal:** se debía a usar una voz en español para todo. Ahora el idioma se
  elige por archivo (sufijo del nombre). Usa `_en` para inglés.
- **Sin internet / edge-tts falla:** se usa automáticamente el backend offline (WAV, SAPI5).
- **Faltan voces offline:** en Windows agrega voces en *Configuración → Hora e idioma → Voz*.
  Las voces "Desktop" SAPI5 son las que ve `pyttsx3`.
- **PDF con texto pobre:** PyPDF2 puede fallar con PDFs complejos; prueba exportarlo a TXT.

## Dependencias
```
edge-tts >= 6.1.9   # voces neurales, MP3, requiere internet
pyttsx3  == 2.90    # voces SAPI5 offline, WAV
PyPDF2   == 3.0.1
python-docx == 1.1.0
```
