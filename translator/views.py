from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .translator import LocalTranslator

# Initialize once (so models load only once)
translator = LocalTranslator()

class EnToNeView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        translation = translator.translate_en_to_ne(text)
        return Response({"input": text, "translation": translation})


class NeToEnView(APIView):
    def post(self, request):
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        translation = translator.translate_ne_to_en(text)
        return Response({"input": text, "translation": translation})
