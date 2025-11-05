# translator/tts.py
from gtts import gTTS
import os

class NepaliTTS:
    def __init__(self, lang="ne"):
        self.lang = lang  # 'ne' for Nepali, 'en' for English

    def synthesize(self, text: str, output_path: str):
        try:
            tts = gTTS(text=text, lang=self.lang)
            tts.save(output_path)
        except Exception as e:
            print(f"TTS generation failed: {e}")
            raise e
