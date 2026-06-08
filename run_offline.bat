@echo off
REM Fuerza el motor offline (SAPI5/pyttsx3). Genera WAV real, sin internet.
REM "set" solo afecta a esta ventana; no queda permanente en el sistema.
set "TTS_ENGINE=offline"
python "%~dp0main.py"
