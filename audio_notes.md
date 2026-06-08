# Audio Notes

## Observación principal

El programa convierte texto a audio y funciona, pero la calidad parece variar por idioma.

- Español: suena aceptable.
- Inglés: suena malo, artificial o con mala pronunciación.

## Sospechas

Puede que el programa esté usando una voz genérica de Windows o una voz configurada para español aunque el texto esté en inglés.

## Lo que quiero revisar

- Si el programa detecta idioma.
- Si permite elegir voz por idioma.
- Si usa voces locales de Windows.
- Si puede usar locale explícito como `es-MX`, `es-ES`, `en-US` o `en-GB`.
- Si conviene usar SSML.
- Si conviene mejorar el preprocesamiento del texto.
- Si conviene separar configuración de voz, idioma y output.

## Nota sobre archivos de audio

Los audios generados previamente son solo ejemplos de output. No deben ser analizados como fuente principal salvo que sea necesario. La prioridad es revisar el código que los genera.