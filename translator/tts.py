# translator/tts.py
from gtts import gTTS

class NepaliTTS:
    def __init__(self, lang="ne"):
        self.lang = lang

    def synthesize(self, text: str, output_path: str):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(output_path)