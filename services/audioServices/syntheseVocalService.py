import os
from enum import Enum
import threading
import os
import time
import threading
from enum import Enum
from gtts import gTTS

AUDIO_DIR = os.path.abspath("./ressources/audio/")


class Langue(Enum):
    EN = "en"
    FR = "fr"

class SyntheseVocalService:
    def __init__(self, language: Langue):
        self.lang = language
        self.lock = threading.Lock()  # Verrou pour synchroniser les accès

    def syntheseVocal(self, text):
        # Créer un nom de fichier unique
        timestamp = str(int(time.time()))
        audio_path = os.path.join(AUDIO_DIR, f"temp_audio_{timestamp}.mp3")
        
        with self.lock:  # Synchroniser les accès
            try:
                # Générer le fichier audio avec gTTS
                tts = gTTS(text=text, lang=self.lang.value)
                tts.save(audio_path)
                print(f"Fichier audio généré : {audio_path}")

                # Lire le fichier audio avec mpg123
                os.system(f"mpg123 {audio_path}")
            except Exception as e:
                print(f"Erreur lors de la synthèse vocale : {e}")
                print(f"Texte à synthétiser : {text}")
            finally:
                # Attendre que la lecture soit terminée avant de supprimer le fichier
                time.sleep(1)  # Délai pour s'assurer que la lecture est terminée
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    print(f"Fichier temporaire supprimé : {audio_path}")
                else:
                    print(f"Fichier temporaire introuvable : {audio_path}")

    def change_lang(self, lang: Langue):
        self.lang = lang