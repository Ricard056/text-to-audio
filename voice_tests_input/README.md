# voice_tests_input — textos de referencia para probar voces

Estos `.txt` son **textos de referencia** para escuchar cómo suena cada **voz edge en-US**.
Cada archivo está redactado en un estilo distinto, según las categorías de
[`docs/voices_en-US.md`](../docs/voices_en-US.md):

| Archivo                 | Estilo / categoría | Voces sugeridas (ejemplos)                 |
|-------------------------|--------------------|--------------------------------------------|
| `cartoon_en.txt`        | Cartoon            | `en-US-AnaNeural`                          |
| `conversation_en.txt`   | Conversation       | `en-US-AvaNeural`, `en-US-BrianNeural`     |
| `news_en.txt`           | News               | `en-US-AriaNeural`, `en-US-ChristopherNeural` |
| `novel_en.txt`          | Novel              | `en-US-GuyNeural`, `en-US-MichelleNeural`  |
| `copilot_en.txt`        | Copilot (asistente)| `en-US-EmmaNeural`, `en-US-AndrewNeural`   |
| `general_en.txt`        | General            | `en-US-JennyNeural`                        |

> **Importante:** esta carpeta **NO se procesa automáticamente**. El programa solo lee
> archivos que estén en `input/`. Estos quedan aquí como referencia hasta que tú copies
> uno a `input/`.

## Cómo probar una voz

1. **Copia** uno de estos `.txt` a la carpeta `input/`
   (por ejemplo `news_en.txt` → `input/news_en.txt`).
2. En `main.py`, cambia **`EDGE_VOICE_EN`** por la voz que quieras probar,
   por ejemplo: `EDGE_VOICE_EN = "en-US-ChristopherNeural"`.
   (Lista de voces: `export_edge_voices.bat` o `edge-tts --list-voices`.)
3. Ejecuta **`run.bat`**. El audio aparecerá en `output/` como `news_en.mp3`.
4. Si quieres **conservar** ese audio, muévelo a **`output__resp_local/`**
   (esa carpeta no se versiona, es tu archivo local de pruebas).

Repite cambiando solo `EDGE_VOICE_EN` para comparar voces con el mismo texto.
El sufijo `_en` en el nombre asegura que se use una voz **inglesa**.
