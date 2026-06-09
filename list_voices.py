"""
Lista las voces disponibles para el conversor.

- Voces OFFLINE (pyttsx3 / SAPI5 de Windows): se listan aquí abajo.
- Voces ONLINE (edge-tts, neurales): se listan con el comando edge-tts (ver recordatorio).

Solo lee información; no modifica nada del proyecto.
Uso: doble clic en list_voices.bat, o `python list_voices.py`.
"""


def list_offline_voices():
    print("=" * 60)
    print("VOCES OFFLINE (pyttsx3 / SAPI5 de Windows)")
    print("=" * 60)
    try:
        import pyttsx3
    except ImportError:
        print("pyttsx3 no está instalado. Ejecuta:  pip install -r requirements.txt")
        return

    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
    except Exception as e:
        print(f"No se pudieron leer las voces offline: {e}")
        return

    if not voices:
        print("No se detectaron voces SAPI5 en este Windows.")
        return

    for idx, v in enumerate(voices):
        langs = ", ".join(str(l) for l in getattr(v, "languages", []) or []) or "?"
        print(f"  [{idx}] {v.name}")
        print(f"       lang={langs}")
        print(f"       id={v.id}")


def edge_reminder():
    print()
    print("=" * 60)
    print("VOCES ONLINE (edge-tts, neurales) - usa estos comandos:")
    print("=" * 60)
    print("  edge-tts --list-voices")
    print("  edge-tts --list-voices | findstr en-US")
    print("  edge-tts --list-voices | findstr es-")
    print()
    print("Para cambiar la voz edge, edita EDGE_VOICE_EN / EDGE_VOICE_MX /")
    print("EDGE_VOICE_ES cerca del inicio de main.py.")


if __name__ == "__main__":
    list_offline_voices()
    edge_reminder()
    input("\nPress Enter to exit...")
