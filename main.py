import os
from controllers.imagesController import app
from services.audioServices.syntheseVocalService import Langue
from services.cameraServices.CaptureService import Camera
from threading import Thread

from services.environmentServices.EnvironmentModel import EnvironmentModel
from services.orchestrationServices.OrcherstrationModel import OrchestrationModel

os.environ["VOSK_MODEL_PATH"] = "./models/vosk-model-small-en-us-0.15"
os.environ["NGROK_URL"] = "https://f689-129-0-60-35.ngrok-free.app"


if __name__ == '__main__':

    camera = Camera()
    camera.change_context("initial")
    capture_Thread = Thread(target=camera.launch_video)
    print("-----------before Camera launched")
    capture_Thread.start()
    print("-----------Camera launched")
    orchestration = OrchestrationModel(camera=camera, langue=Langue.EN)  # Choisir la langue (EN ou FR)
    print("-----------before Orchestration launched")
    try:
        orchestration.lancer_conversation()
    except Exception as e:
        print(f"Erreur lors du lancement de la conversation : {e}")
    print("-----------Conversation launched")

