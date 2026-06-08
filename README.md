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

## Configuración

Edita las constantes al inicio de `main.py`:

```python
ENGINE = "edge"            # "edge" (neural, MP3, internet) o "offline" (SAPI5, WAV)
DEFAULT_LANGUAGE = "es-MX" # idioma para archivos sin sufijo reconocido
SPEECH_RATE = 150          # solo backend offline: 100=lento, 150=normal, 200=rápido
VOLUME = 1.0               # solo backend offline: 0.0 a 1.0
```

Las voces por idioma se definen en `LANGUAGE_MAP` (puedes cambiarlas).
Para ver las voces neurales disponibles:
```bash
edge-tts --list-voices
```

## Estructura
```
20250816_text_to_audio/
├── main.py           # lógica + configuración
├── setup.py          # instala dependencias y crea carpetas
├── requirements.txt
├── CLAUDE.md         # mapa del proyecto
├── README.md
├── audio_notes.md
├── input/            # tus archivos (sufijo = idioma)
└── output/           # audio generado (no versionado)
```

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
