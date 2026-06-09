"""
Text to Audio Converter
Date: 2025-08-16
Description: Converts text files (TXT, PDF, DOCX) to audio.

Two TTS backends:
  - "edge"    : edge-tts neural voices (high quality, free, no API key, needs internet).
                Outputs real MP3.
  - "offline" : pyttsx3 / Windows SAPI5 voices (works offline, lower quality).
                Outputs real WAV.

Language (and therefore voice) is chosen PER FILE from the filename suffix
(e.g. report_en.txt -> English, nota_mx.txt -> Spanish Mexico).
"""

import asyncio
import os
from pathlib import Path

import PyPDF2
from docx import Document

# ==============================================================================
# USER CONFIGURATION SECTION - MODIFY THESE SETTINGS AS NEEDED
# ==============================================================================

# Folder paths (relative to script location)
INPUT_FOLDER = "input"       # Place your text files here
OUTPUT_FOLDER = "output"     # Audio files will be saved here

# TTS backend (override without editing code via env var TTS_ENGINE, e.g. run_offline.bat):
#   "edge"    -> neural voices, real MP3, needs internet (falls back to offline on failure)
#   "offline" -> Windows SAPI5 voices, real WAV, no internet
ENGINE = os.getenv("TTS_ENGINE", "edge").strip().lower()
if ENGINE not in {"edge", "offline"}:
    print(f"[WARN] Unknown TTS_ENGINE={ENGINE!r}; using offline mode.")
    ENGINE = "offline"

# Used only by the offline (pyttsx3) backend
SPEECH_RATE = 150            # Normal: 150, slower: 100, faster: 200
VOLUME = 1.0                 # Range: 0.0 to 1.0

# Language used when a file has no recognizable suffix (must be a key of LANGUAGE_MAP)
DEFAULT_LANGUAGE = "es-MX"

# --- Voces edge-tts -----------------------------------------------------------
# Para cambiar voces, edita SOLO estas constantes.
# Para ver las voces online actuales: corre export_edge_voices.bat
#   (o:  edge-tts --list-voices  /  edge-tts --list-voices | findstr en-US )
# Después de cambiar una voz, corre run.bat y prueba con un archivo _en/_mx/_es.
EDGE_VOICE_EN = "en-US-AriaNeural"    # Inglés (en-US)         - voz femenina
EDGE_VOICE_MX = "es-MX-DaliaNeural"   # Español México (es-MX) - voz femenina
EDGE_VOICE_ES = "es-ES-ElviraNeural"  # Español España (es-ES) - voz femenina

# Language map: locale -> how to detect it and which voice to use per backend.
#   suffixes      : filename endings (lowercase) that map to this locale
#   edge_voice    : neural voice for edge-tts (edita arriba: EDGE_VOICE_*)
#   offline_match : substrings searched in SAPI5 voice name/id (first match wins)
LANGUAGE_MAP = {
    # offline_match is tried in order; put the most specific terms first
    # (locale token, then known voice names) so generic ones never win early.
    "en-US": {
        "suffixes": ["_en", "_us", "_en-us"],
        "edge_voice": EDGE_VOICE_EN,
        "offline_match": ["en-us", "en_us", "zira", "david", "hazel", "english", "en-"],
    },
    "es-MX": {
        "suffixes": ["_mx", "_es-mx"],
        "edge_voice": EDGE_VOICE_MX,
        "offline_match": ["es-mx", "es_mx", "sabina", "raul", "spanish", "es-"],
    },
    "es-ES": {
        "suffixes": ["_es", "_es-es"],
        "edge_voice": EDGE_VOICE_ES,
        "offline_match": ["es-es", "es_es", "helena", "laura", "spanish", "es-"],
    },
}

# File processing
SUPPORTED_FORMATS = [".txt", ".pdf", ".docx"]
PROCESS_ALL_FILES = True     # True: process all files, False: ask for each file

# ==============================================================================
# END OF USER CONFIGURATION
# ==============================================================================

# Suffix -> locale lookup, longest suffix first so "_es-mx" wins over "_mx".
SUFFIX_TO_LOCALE = sorted(
    ((suffix, locale) for locale, cfg in LANGUAGE_MAP.items() for suffix in cfg["suffixes"]),
    key=lambda pair: len(pair[0]),
    reverse=True,
)


def detect_language(stem):
    """Return a locale (key of LANGUAGE_MAP) from the filename stem, or DEFAULT_LANGUAGE."""
    name = stem.lower()
    for suffix, locale in SUFFIX_TO_LOCALE:
        if name.endswith(suffix):
            return locale
    return DEFAULT_LANGUAGE


class TextToAudioConverter:
    def __init__(self):
        print("[INIT] Initializing Text-to-Audio Converter...")
        self.setup_folders()
        if DEFAULT_LANGUAGE not in LANGUAGE_MAP:
            raise ValueError(f"DEFAULT_LANGUAGE '{DEFAULT_LANGUAGE}' is not a key of LANGUAGE_MAP")
        print(f"[ENGINE] Backend: {ENGINE}")
        print("[INIT] Initialization complete!")
        print("-" * 50)

    def setup_folders(self):
        script_dir = Path(__file__).parent
        self.input_path = script_dir / INPUT_FOLDER
        self.output_path = script_dir / OUTPUT_FOLDER
        self.input_path.mkdir(exist_ok=True)
        self.output_path.mkdir(exist_ok=True)
        print(f"[SETUP] Input folder: {self.input_path}")
        print(f"[SETUP] Output folder: {self.output_path}")

    # ----------------------------------------------------------------- readers
    def read_txt_file(self, filepath):
        """Read a text file, trying a few common encodings before giving up."""
        print(f"[READ] Reading TXT file: {filepath.name}")
        for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                with open(filepath, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        print(f"[ERROR] Could not decode {filepath.name} with known encodings")
        return None

    def read_pdf_file(self, filepath):
        print(f"[READ] Reading PDF file: {filepath.name}")
        text = ""
        try:
            with open(filepath, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                print(f"[PDF] Processing {num_pages} pages...")
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text += (page.extract_text() or "") + "\n"
                    if page_num % 10 == 0:
                        print(f"[PDF] Processed {page_num}/{num_pages} pages")
        except Exception as e:
            print(f"[ERROR] Failed to read PDF: {e}")
            return None
        return text

    def read_docx_file(self, filepath):
        print(f"[READ] Reading DOCX file: {filepath.name}")
        try:
            doc = Document(filepath)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        except Exception as e:
            print(f"[ERROR] Failed to read DOCX: {e}")
            return None

    def read_file(self, filepath):
        extension = filepath.suffix.lower()
        if extension == ".txt":
            return self.read_txt_file(filepath)
        if extension == ".pdf":
            return self.read_pdf_file(filepath)
        if extension == ".docx":
            return self.read_docx_file(filepath)
        print(f"[ERROR] Unsupported file format: {extension}")
        return None

    # ----------------------------------------------------------------- backends
    def synthesize_edge(self, text, voice, output_path):
        """Neural TTS via edge-tts. Produces a real MP3. Returns True on success."""
        import edge_tts

        async def _run():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_path))

        try:
            asyncio.run(_run())
            if output_path.exists() and output_path.stat().st_size > 0:
                return True
            # Empty/partial file: remove it so it doesn't sit next to the WAV fallback.
            self._cleanup_partial(output_path)
            return False
        except Exception as e:
            print(f"[WARN] edge-tts failed ({e}). Falling back to offline engine.")
            self._cleanup_partial(output_path)
            return False

    def synthesize_offline(self, text, locale_cfg, output_path):
        """Offline TTS via pyttsx3/SAPI5. Produces a real WAV. Returns True on success.

        A fresh engine is created per call: reusing one engine across multiple
        save_to_file/runAndWait calls is a known pyttsx3 cause of empty output files.
        """
        import pyttsx3

        engine = pyttsx3.init()
        try:
            engine.setProperty("rate", SPEECH_RATE)
            engine.setProperty("volume", VOLUME)

            voices = engine.getProperty("voices")
            selected = self._select_offline_voice(voices, locale_cfg["offline_match"])
            if selected is not None:
                engine.setProperty("voice", selected.id)
                print(f"[VOICE] Offline voice: {selected.name}")
            else:
                print("[WARN] No SAPI5 voice matched this language; using system default.")

            engine.save_to_file(text, str(output_path))
            engine.runAndWait()
            return output_path.exists() and output_path.stat().st_size > 0
        except Exception as e:
            print(f"[ERROR] Offline synthesis failed: {e}")
            return False
        finally:
            try:
                engine.stop()
            except Exception:
                pass

    @staticmethod
    def _select_offline_voice(voices, match_terms):
        """Pick a SAPI5 voice, honoring term priority: the most specific term
        (e.g. "es-mx") wins over generic ones (e.g. "spanish") regardless of the
        order the OS lists its voices."""
        haystacks = [(v, f"{v.name} {v.id}".lower()) for v in voices]
        for term in match_terms:
            for voice, haystack in haystacks:
                if term in haystack:
                    return voice
        return None

    @staticmethod
    def _cleanup_partial(path):
        """Remove a leftover empty/partial output file, ignoring errors."""
        try:
            if path.exists():
                path.unlink()
        except OSError:
            pass

    # ----------------------------------------------------------------- pipeline
    def text_to_audio(self, text, base_name):
        """Convert text to audio using the configured backend (with fallback)."""
        if not text or not text.strip():
            print("[ERROR] No text to convert!")
            return False

        locale = detect_language(base_name)
        locale_cfg = LANGUAGE_MAP[locale]
        print(f"[LANG] {base_name} -> {locale}")
        print(f"[CONVERT] Text length: {len(text)} characters")

        # edge-tts -> real MP3; offline -> real WAV. Extension always matches reality.
        if ENGINE == "edge":
            mp3_path = self.output_path / f"{base_name}.mp3"
            if self.synthesize_edge(text, locale_cfg["edge_voice"], mp3_path):
                print(f"[SUCCESS] Audio saved to: {mp3_path}")
                return True
            # fall through to offline

        wav_path = self.output_path / f"{base_name}.wav"
        if self.synthesize_offline(text, locale_cfg, wav_path):
            print(f"[SUCCESS] Audio saved to: {wav_path}")
            return True

        print("[FAILED] Could not generate audio for this file.")
        return False

    def process_file(self, filepath):
        print(f"\n[PROCESS] Processing: {filepath.name}")
        print("-" * 30)
        try:
            text = self.read_file(filepath)
            if not text:
                print(f"[SKIP] Skipping {filepath.name} - Could not read file")
                return
            if self.text_to_audio(text, filepath.stem):
                print(f"[COMPLETE] Successfully processed {filepath.name}")
            else:
                print(f"[FAILED] Failed to process {filepath.name}")
        except Exception as e:
            # One bad file must never abort the whole batch.
            print(f"[ERROR] Unexpected error on {filepath.name}: {e}")

    def run(self):
        print("\n" + "=" * 50)
        print("STARTING TEXT TO AUDIO CONVERSION")
        print("=" * 50)

        files = []
        for ext in SUPPORTED_FORMATS:
            files.extend(self.input_path.glob(f"*{ext}"))

        if not files:
            print(f"\n[WARNING] No supported files found in {self.input_path}")
            print(f"[INFO] Supported formats: {', '.join(SUPPORTED_FORMATS)}")
            print(f"[INFO] Add files to the '{INPUT_FOLDER}' folder and run again.")
            return

        print(f"\n[FOUND] {len(files)} file(s) to process:")
        for idx, file in enumerate(files, 1):
            print(f"  {idx}. {file.name}")

        if PROCESS_ALL_FILES:
            print("\n[MODE] Processing all files automatically...")
            for file in files:
                self.process_file(file)
        else:
            for file in files:
                if input(f"\nProcess {file.name}? (y/n): ").strip().lower() == "y":
                    self.process_file(file)
                else:
                    print(f"[SKIP] Skipping {file.name}")

        print("\n" + "=" * 50)
        print("CONVERSION COMPLETE!")
        print(f"Check the '{OUTPUT_FOLDER}' folder for your audio files.")
        print("=" * 50)


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    try:
        converter = TextToAudioConverter()
        converter.run()
    except KeyboardInterrupt:
        print("\n\n[INTERRUPT] Process cancelled by user.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] {e}")
        print("Please check your configuration and try again.")

    input("\nPress Enter to exit...")
