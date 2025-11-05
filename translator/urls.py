# translator/urls.py
from django.urls import path
from .views import TextTranslateView, SpeechTranslateView

urlpatterns = [
    path("translate/text/", TextTranslateView.as_view(), name="text-translate"),
    path("translate/speech/", SpeechTranslateView.as_view(), name="speech-translate"),
]