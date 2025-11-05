# translator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .translator import LocalTranslator
from .pipeline import SpeechTranslator

translator = LocalTranslator()
speech_translator = SpeechTranslator()
    
# TEXT TRANSLATION
class TextTranslateView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        direction = request.data.get("direction", "en2ne")
        if not text:
            return Response({"error": "No text"}, status=400)

        if direction == "en2ne":
            result = translator.translate_en_to_ne(text)
        else:
            result = translator.translate_ne_to_en(text)

        return Response({"input": text, "translation": result, "direction": direction})

# translator/views.py
class SpeechTranslateView(APIView):
    def post(self, request):
        audio = request.FILES.get("audio")

        if not audio:
            return Response({"error": "No audio file"}, status=400)

        try:
            result = speech_translator.speech_to_speech(audio)
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

