import os
from gtts import gTTS

IMAGE_DIR = os.path.abspath("../ressources/audio")

_lang = {
    "en": "en",
    "fr": "fr"
}


class SyntheseVocalService:

    def __init__(self, language: _lang):
        self.lang = language

    def syntheseVocal(self, text):
        tts = gTTS(text=text, lang=self.lang)
        # Sauvegarder l'audio dans un fichier temporaire
        tts.save(IMAGE_DIR + "temp_audio.mp3")
        os.system("mpg123 temp_audio.mp3")

    def change_lang(self, lang: _lang):
        self.lang = lang
