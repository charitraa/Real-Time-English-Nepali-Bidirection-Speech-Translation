# translator/pipeline.py
import uuid
from .asr import ASR
from .translator import LocalTranslator
from .tts import NepaliTTS
import os

class SpeechTranslator:
    def __init__(self):
        self.asr = ASR(model_size="small")
        self.translator = LocalTranslator()

    def speech_to_speech(self, audio_file):
        temp_dir = "temp_audio"
        os.makedirs(temp_dir, exist_ok=True)
        input_path = os.path.join(temp_dir, f"input_{uuid.uuid4().hex}.wav")

        # ✅ Write uploaded file to disk
        with open(input_path, "wb+") as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # 1️⃣ ASR: auto detect language
        recognized_text, detected_lang = self.asr.transcribe(input_path)

        # 2️⃣ Determine translation direction automatically
        if detected_lang.startswith("en"):
            direction = "en2ne"
        else:
            direction = "ne2en"

        # 3️⃣ Translate
        if direction == "en2ne":
            translated_text = self.translator.translate_en_to_ne(recognized_text)
            tts_lang = "ne"
        else:
            translated_text = self.translator.translate_ne_to_en(recognized_text)
            tts_lang = "en"

        # 4️⃣ TTS using gTTS
        output_path = os.path.join(temp_dir, f"output_{uuid.uuid4().hex}.mp3")
        tts_engine = NepaliTTS(lang=tts_lang)
        tts_engine.synthesize(translated_text, output_path)

        # 5️⃣ Return response
        return {
            "detected_language": detected_lang,
            "recognized_text": recognized_text,
            "translation": translated_text,
            "output_audio": f"/temp_audio/{os.path.basename(output_path)}"
        }

