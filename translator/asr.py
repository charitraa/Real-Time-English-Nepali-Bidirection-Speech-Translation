# translator/asr.py
from faster_whisper import WhisperModel
import os
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

class ASR:
    def __init__(self, model_size="small"):
        use_gpu = bool(os.getenv("USE_GPU", "0"))  # Default: CPU (0)
        
        if use_gpu:
            try:
                # Test CUDA availability
                import torch
                if not torch.cuda.is_available():
                    raise RuntimeError("CUDA not available")
                device = "cuda"
                compute_type = "float16"
                print("✅ Using GPU for Whisper")
            except Exception as e:
                print(f"⚠️ GPU failed ({e}), falling back to CPU")
                use_gpu = False
                device = "cpu"
                compute_type = "int8"
        else:
            device = "cpu"
            compute_type = "int8"
            print("✅ Using CPU for Whisper (set USE_GPU=1 for GPU)")

        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        print(f"✅ Loaded Whisper ({model_size}) on {device.upper()} with {compute_type}")

    def transcribe(self, audio_path: str, language: str = None) -> tuple:
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            vad_filter=True
        )

        text = " ".join([seg.text for seg in segments]).strip()
        detected_lang = info.language if info else (language or "unknown")

        if not text:
            return "", detected_lang

        try:
            text_lang = detect(text)
            if detected_lang == "en" and text_lang != "en":
                print(f"⚠️ Override: {detected_lang} → {text_lang}")
                detected_lang = text_lang
            elif detected_lang.startswith("ne") and text_lang == "en":
                detected_lang = "en"
        except Exception as e:
            print(f"⚠️ Lang detect failed: {e}")

        return text, detected_lang