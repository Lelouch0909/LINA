import os
from time import sleep

from controllers.imagesController import app
from services.audioServices.syntheseVocalService import Langue
from services.cameraServices.CaptureService import Camera
from threading import Thread

from services.environmentServices.EnvironmentModel import EnvironmentModel
from services.orchestrationServices.OrcherstrationModel import OrchestrationModel

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
os.environ["VOSK_MODEL_PATH"] = "./models/vosk-model-small-en-us-0.15"
os.environ["NGROK_URL"] = "https://a91c-129-0-60-56.ngrok-free.app"


if __name__ == '__main__':

    camera = Camera()
    camera.change_context("initial")
    capture_Thread = Thread(target=camera.launch_video)
    print("-----------before Camera launched")
    capture_Thread.start()
    print("-----------Camera launched")
    orchestration = OrchestrationModel(langue=Langue.EN)  # Choisir la langue (EN ou FR)
    print("-----------before Orchestration launched")
    orchestration.lancer_conversation()
    print("-----------Conversation launched")

