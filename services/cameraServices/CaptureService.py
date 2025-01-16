import os
import threading
import cv2
from pprint import pprint

class Camera:
    _instance_lock = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not cls._instance:
                cls._instance = super(Camera, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'cap'):
            self.cap = cv2.VideoCapture('http://192.168.1.111:81/stream')  # Utiliser la caméra par défaut
            self.pause_reading = threading.Event()
            self.resume_reading = threading.Event()
            self.save_dir = os.path.abspath("ressources/videos")
            self._context = "initial"
            self._index = 0
            self.save_path = os.path.join(self.save_dir, self._context)
            self.create_dir(self.save_path)

    @property
    def get_context(self):
        """Retourne le contexte actuel de la caméra."""
        return self._context

    @property
    def get_index(self):
        """Retourne l'index de la dernière frame enregistrée."""
        return self._index

    def create_dir(self, path):
        """Crée un répertoire s'il n'existe pas."""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Répertoire créé : {path}")
        except OSError as exc:
            print(f"Erreur OS lors de la création du répertoire : {exc}")

    def launch_video(self):
        """Lance l'enregistrement des frames de la caméra."""
        self._index = 0
        if not self.cap.isOpened():
            print("Erreur : Impossible d'ouvrir le flux vidéo.")
            return

        try:
            while True:
                if not self.pause_reading.is_set():
                    ret, frame = self.cap.read()
                    if not ret:
                        print("Erreur : Impossible de lire la frame.")
                        break

                    # Enregistrer la frame
                    frame_path = f"{self.save_path}/{self._index}.png"
                    cv2.imwrite(frame_path, frame)
                    self._index += 1

                    # Vérifier et nettoyer les anciennes images si nécessaire
                    self.cleanup_old_images()
                else:
                    # Mettre en pause l'enregistrement
                    self.resume_reading.wait()
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des frames : {e}")
        finally:
            self.cap.release()
            print("Flux vidéo libéré.")

    def cleanup_old_images(self):
        """Supprime les 100 images les plus anciennes si le dossier contient plus de 200 images."""
        try:
            # Lister tous les fichiers dans le dossier
            files = sorted(os.listdir(self.save_path), key=lambda x: os.path.getmtime(os.path.join(self.save_path, x)))

            # Vérifier si le nombre d'images dépasse 200
            if len(files) > 1000:
                # Supprimer les 100 images les plus anciennes
                for file in files[:500]:
                    file_path = os.path.join(self.save_path, file)
                    os.remove(file_path)

                # Mettre à jour l'index
                self._index = len(files) - 100
        except Exception as e:
            print(f"Erreur lors du nettoyage des anciennes images : {e}")

    def pause_video(self):
        """Met en pause l'enregistrement des frames."""
        self.pause_reading.set()
        self.resume_reading.clear()
        pprint("Enregistrement en pause")

    def resume_video(self):
        """Reprend l'enregistrement des frames."""
        self.pause_reading.clear()
        self.resume_reading.set()
        pprint("Enregistrement repris")

    def change_context(self, context_room):
        """Change le contexte de la caméra (répertoire d'enregistrement)."""
        self._context = context_room
        self.save_path = os.path.join(self.save_dir, self._context)
        self.create_dir(self.save_path)
        print(f"Contexte changé pour : {self._context}")