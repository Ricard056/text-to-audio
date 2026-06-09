@echo off
REM Guarda una referencia local de las voces edge-tts (online) en la carpeta docs\.
REM No afecta main.py ni el flujo de conversion: solo crea archivos de consulta.

set "DOCSDIR=%~dp0docs"
if not exist "%DOCSDIR%" mkdir "%DOCSDIR%"

set "F_EN=%DOCSDIR%\voices_en-US.md"
set "F_ES=%DOCSDIR%\voices_es.md"

REM --- Ingles (en-US) ---
>"%F_EN%" echo # Voces edge-tts - en-US
>>"%F_EN%" echo.
>>"%F_EN%" echo Generado: %DATE% %TIME%
>>"%F_EN%" echo.
>>"%F_EN%" echo Para usar una voz, copia su nombre a EDGE_VOICE_EN en main.py.
>>"%F_EN%" echo.
>>"%F_EN%" echo ```
edge-tts --list-voices | findstr en-US >>"%F_EN%"
>>"%F_EN%" echo ```

REM --- Espanol (es-) ---
>"%F_ES%" echo # Voces edge-tts - espanol (es-)
>>"%F_ES%" echo.
>>"%F_ES%" echo Generado: %DATE% %TIME%
>>"%F_ES%" echo.
>>"%F_ES%" echo Para usar una voz, copia su nombre a EDGE_VOICE_MX o EDGE_VOICE_ES en main.py.
>>"%F_ES%" echo.
>>"%F_ES%" echo ```
edge-tts --list-voices | findstr es- >>"%F_ES%"
>>"%F_ES%" echo ```

echo.
echo Referencias generadas en:
echo   %F_EN%
echo   %F_ES%
echo.
pause
