import json
import os
import pyaudio
from vosk import KaldiRecognizer, Model

os.environ["VOSK_MODEL_PATH"] = "/home/lelouch/VscodeWorkspace/LINA/models//vosk-model-small-en-us-0.15/"
class ReconnaissanceVocalModel:
    def __init__(self, keywords=["nina"]):
        self.model = Model(os.getenv("VOSK_MODEL_PATH"))
        self.reconnaisseur = KaldiRecognizer(self.model, 16000)
        self.keywords = [keyword.lower() for keyword in keywords]
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def commencer_l_ecoute(self):
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )
        self.stream.start_stream()
        print(f"En attente des mots clés : {', '.join(self.keywords)} ...")

    def ecouter_et_enregistrer(self):
        enregistrement = ""
        mot_cle_detecte = False

        while True:
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.reconnaisseur.AcceptWaveform(data):
                result = json.loads(self.reconnaisseur.Result())
                texte = result.get("text", "").lower()
                print(f"Texte reconnu : {texte}")

                # Détecter le mot-clé
                if not mot_cle_detecte:
                    for keyword in self.keywords:
                        if keyword in texte:
                            print(f"Mot-clé {keyword} détecté. Enregistrement en cours...")
                            mot_cle_detecte = True
                            enregistrement = texte.replace(keyword, "").strip()  # Supprimer le mot-clé
                            break
                else:
                    # Si un mot-clé a été détecté, continuer à enregistrer
                    enregistrement += " " + texte

                    # Détecter la fin de la parole
                    if self.detecter_fin_de_parole():
                        print("Fin de la parole détectée.")
                        return self.nettoyer_texte(enregistrement.strip())

    def detecter_fin_de_parole(self, silence_seuil=0):
        silence_duree = 0
        for _ in range(silence_seuil + 1):
            data = self.stream.read(4096, exception_on_overflow=False)
            if self.reconnaisseur.AcceptWaveform(data):
                return False
            if not data.strip():
                silence_duree += 1
            else:
                silence_duree = 0
        return True

    def arreter_ecoute(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        
    def nettoyer_texte(self,texte):
            # Supprimer les mots en double et les phrases inutiles
            mots = texte.split()
            mots_uniques = []
            for mot in mots:
                if mot not in mots_uniques:
                    mots_uniques.append(mot)
            return " ".join(mots_uniques)

