from faster_whisper import WhisperModel
import os
from langdetect import detect, DetectorFactory

# Fix random seed for consistent detection
DetectorFactory.seed = 0


class ASR:
    def __init__(self, model_size="small"):
        # Detect GPU availability
        use_gpu = bool(os.getenv("USE_GPU"))

        # Choose compute type based on hardware
        compute_type = "float16" if use_gpu else "float32"

        # Load Whisper model
        self.model = WhisperModel(
            model_size,
            device="cuda" if use_gpu else "cpu",
            compute_type=compute_type
        )
        print(f"✅ Loaded Whisper model ({model_size}) on {'GPU' if use_gpu else 'CPU'} with {compute_type}")

    def transcribe(self, audio_path: str, language: str = None) -> tuple:
        """
        Transcribe an audio file and detect language.
        If Whisper misdetects (e.g., short Nepali phrase → English), 
        fallback to text-based detection.
        """

        # 1️⃣ Run Whisper transcription (auto or forced language)
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )

        text = " ".join([seg.text for seg in segments]).strip()
        detected_lang = info.language if info else (language or "unknown")

        # 2️⃣ Handle edge cases (short or mixed-language phrases)
        if not text:
            return "", detected_lang

        try:
            # Re-check detected language from transcribed text
            text_lang = detect(text)

            # If Whisper says "en" but langdetect says Nepali, override
            if detected_lang == "en" and text_lang not in ["en"]:
                print(f"⚠️ Overriding Whisper language {detected_lang} → {text_lang}")
                detected_lang = text_lang

            # If Whisper says Nepali but text is mostly English, fix too
            elif detected_lang.startswith("ne") and text_lang == "en":
                print(f"⚠️ Overriding Whisper language {detected_lang} → en")
                detected_lang = "en"

        except Exception as e:
            print(f"⚠️ Language detection fallback failed: {e}")

        return text, detected_lang
