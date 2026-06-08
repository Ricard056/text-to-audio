# Guía de uso y prueba

Guía paso a paso para usar y probar el conversor de texto a audio en **Windows**.
Pensada para cualquier usuario, no hace falta saber programar.

---

## 1. ¿Qué hace el programa?

Convierte archivos de texto `.txt` que pongas en la carpeta **`input/`** en archivos de
**audio** que aparecen en la carpeta **`output/`**.

- Elige automáticamente el idioma y la voz según el **nombre del archivo** (ver sección 3).
- También acepta `.pdf` y `.docx`, pero en esta guía usamos `.txt` por simplicidad.

---

## 2. Estructura básica de carpetas

```
20250816_text_to_audio/
├── input/             ← aquí pones tus archivos de texto
├── output/            ← aquí aparecen los audios generados
├── main.py            ← el programa (no necesitas abrirlo)
├── run.bat            ← ejecutar en modo normal (doble clic)
├── run_offline.bat    ← ejecutar en modo offline (doble clic)
└── requirements.txt   ← lista de dependencias (se instalan una vez)
```

Si no ves la carpeta `output/`, no te preocupes: el programa la crea sola al ejecutarse.

---

## 3. Cómo preparar tus archivos de entrada

El **idioma se decide por el final del nombre del archivo** (el sufijo antes de `.txt`):

| Termina en… | Idioma que usa        | Ejemplo de nombre   |
|-------------|-----------------------|---------------------|
| `_en`       | Inglés (en-US)        | `archivo_en.txt`    |
| `_mx`       | Español de México     | `archivo_mx.txt`    |
| `_es`       | Español de España     | `archivo_es.txt`    |
| (sin sufijo)| El idioma por defecto*| `archivo.txt`       |

\* El idioma por defecto (`DEFAULT_LANGUAGE`) viene configurado como **español de México (es-MX)**.

### Ejemplos CORRECTOS ✅
- `noticias_en.txt` → inglés
- `receta_mx.txt` → español México
- `carta_es.txt` → español España
- `cuento_mx.txt` → español México

### Ejemplos INCORRECTOS ❌ (no se detecta bien el idioma)
- `english.txt` → **no** termina en `_en`; usará el idioma por defecto (español).
- `texto-en.txt` → usa guion en vez de guion bajo; **no** cuenta.
- `EN_archivo.txt` → el sufijo va al **final**, no al principio.
- `archivo_en (1).txt` → termina en `(1)`, no en `_en`.

> Regla de oro: el nombre debe **terminar** exactamente en `_en`, `_mx` o `_es` justo antes
> de `.txt`. Usa guion bajo `_`, no guion `-` ni espacio.

---

## 4. Cómo ejecutar en modo NORMAL (recomendado)

**Opción A – Doble clic:**
1. Abre la carpeta del proyecto en el Explorador de Windows.
2. Haz doble clic en **`run.bat`**.
3. Se abre una ventana negra que muestra el progreso. Espera a que diga `CONVERSION COMPLETE!`.
4. Pulsa Enter para cerrar.

**Opción B – Desde la terminal:**
```bat
python main.py
```

**¿Qué hace el modo normal?**
- Usa **edge-tts** (voces neurales de Microsoft, suenan muy naturales).
- Genera **MP3 real**.
- **Requiere internet.**
- Si edge-tts falla (por ejemplo, sin internet), **cae automáticamente al modo offline** y
  genera un **WAV real** en su lugar. No tienes que hacer nada.

---

## 5. Cómo ejecutar en modo OFFLINE (sin internet)

**Opción A – Doble clic:**
1. Haz doble clic en **`run_offline.bat`**.
2. Espera a que diga `CONVERSION COMPLETE!` y pulsa Enter.

**Opción B – Desde la terminal:**
```bat
set TTS_ENGINE=offline
python main.py
```

**¿Qué hace el modo offline?**
- Usa **pyttsx3 / voces SAPI5 de Windows** (las voces instaladas en tu sistema).
- **No requiere internet.**
- Genera **WAV real**.
- La calidad es más básica que edge-tts, pero funciona siempre.

---

## 6. Cómo saber si funcionó

1. Abre la carpeta **`output/`**.
2. Busca el archivo con el **mismo nombre** que tu texto:
   - Termina en **`.mp3`** → lo generó **edge-tts** (modo normal con internet).
   - Termina en **`.wav`** → lo generó el **modo offline** (o el fallback automático).
3. Comprueba que el archivo **no pese 0 KB** (si pesa 0, algo falló; ver sección 8).
4. Ábrelo con cualquier reproductor (o cópialo al celular) y escúchalo.

> Ejemplo: `input/receta_mx.txt` con modo normal → `output/receta_mx.mp3`.

---

## 7. Prueba mínima recomendada

1. En `input/`, crea **`test_en.txt`** con una frase en inglés, por ejemplo:
   ```
   Hello, this is a quick English test. Can you hear me clearly?
   ```
2. En `input/`, crea **`test_mx.txt`** con una frase en español, por ejemplo:
   ```
   Hola, esta es una prueba rápida en español. ¿Se escucha bien?
   ```
3. Haz doble clic en **`run.bat`** (modo normal, internet).
4. Revisa `output/`: deberías ver **`test_en.mp3`** y **`test_mx.mp3`**.
5. Ahora haz doble clic en **`run_offline.bat`** (modo offline).
6. Revisa `output/`: ahora también aparecen **`test_en.wav`** y **`test_mx.wav`**.
7. Escucha los cuatro: el inglés debe sonar en voz inglesa y el español en voz española.

---

## 8. Qué hacer si algo falla

| Problema | Qué hacer |
|---|---|
| **No hay internet** | Usa `run_offline.bat`. O deja que `run.bat` caiga solo al modo offline (generará `.wav`). |
| **Faltan dependencias** | Abre una terminal en la carpeta y ejecuta: `pip install -r requirements.txt` (o `python setup.py`). |
| **"python no se reconoce"** | Python no está instalado o no está en el PATH. Instálalo desde python.org y marca **"Add Python to PATH"** durante la instalación. |
| **Las voces offline suenan mal** | Es normal: son las voces básicas de Windows. Para mejor calidad usa el modo normal (edge-tts). También puedes instalar más voces en *Configuración → Hora e idioma → Voz*. |
| **El audio sale en idioma incorrecto** | Revisa el **nombre del archivo**: debe terminar en `_en`, `_mx` o `_es` (sección 3). Renómbralo y vuelve a ejecutar. |
| **No aparece la carpeta `output/`** | Se crea sola al ejecutar. Si no aparece, revisa que el programa terminó sin errores (lee la ventana negra). |
| **El audio pesa 0 KB** | El texto estaba vacío o hubo un error de red. Revisa que el `.txt` tenga contenido y vuelve a intentar. |

---

## 9. Archivos que SÍ puedes tocar normalmente

- **`input/`** → agrega, renombra o borra tus archivos de texto libremente.
- **`output/`** → puedes borrar audios viejos cuando quieras.
- **`LANGUAGE_MAP`** (dentro de `main.py`) → solo si quieres **cambiar las voces** por idioma.
  Las voces neurales actuales son: inglés `en-US-AriaNeural`, México `es-MX-DaliaNeural`,
  España `es-ES-ElviraNeural`. Para ver otras voces disponibles, en la terminal:
  ```bat
  edge-tts --list-voices
  ```

---

## 10. Archivos que NO deberías tocar normalmente

- **`main.py`** → es el programa. No lo edites salvo cambios controlados (como `LANGUAGE_MAP`).
- **`requirements.txt`** → solo se usa para instalar dependencias; no lo edites a mano.
- **`CLAUDE.md`** → documentación interna del proyecto; no es para uso diario.

---

## 11. Nota sobre `TTS_ENGINE`

`TTS_ENGINE` es una variable que decide qué motor de voz se usa. Normalmente **no necesitas
tocarla** (los `.bat` ya la manejan), pero por si acaso:

- `TTS_ENGINE=edge` → modo normal (voces neurales, MP3, internet). **Es el valor por defecto.**
- `TTS_ENGINE=offline` → fuerza el modo offline (voces de Windows, WAV, sin internet).
- Cualquier **otro valor** → el programa **avisa** y usa el modo offline por seguridad.

`run_offline.bat` solo pone esta variable temporalmente para esa ejecución; **no cambia nada
permanente** en tu Windows.
