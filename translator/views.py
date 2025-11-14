# translator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .translator import LocalTranslator
from .pipeline import SpeechTranslator
import threading

# Global instances (but lazy-init)
translator = LocalTranslator()
_speech_translator = None
_speech_lock = threading.Lock()

def get_speech_translator():
    global _speech_translator
    if _speech_translator is None:
        with _speech_lock:
            if _speech_translator is None:
                _speech_translator = SpeechTranslator()
    return _speech_translator

class TextTranslateView(APIView):
    def post(self, request):
        text = request.data.get("text", "").strip()
        direction = request.data.get("direction", "en2ne")

        if not text:
            return Response({"error": "No text provided"}, status=400)

        if direction == "en2ne":
            result = translator.translate_en_to_ne(text)
        else:
            result = translator.translate_ne_to_en(text)

        return Response({
            "input": text,
            "translation": result,
            "direction": direction
        })

class SpeechTranslateView(APIView):
    def post(self, request):
        audio = request.FILES.get("audio")
        if not audio:
            return Response({"error": "No audio file provided"}, status=400)

        try:
            speech_translator = get_speech_translator()  # Lazy load here
            result = speech_translator.speech_to_speech(audio)
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)