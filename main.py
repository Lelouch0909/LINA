from controllers.imagesController import app
from services.cameraServices.CaptureService import Camera
from threading import Thread

from services.environmentServices.EnvironmentModel import EnvironmentModel

if __name__ == '__main__':
    # Lancement du serveur pour rendre les images accessibles
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.start()

    # Lancement de la camera
    camera = Camera()
    # On attribut un contexte qui correspond en bref a la piece dans laquelle il se trouve et qui correspond a un
    # nom de dossier
    camera.change_context("initial")
    # On lance la lecture de la camera a partir d un thread
    capture_Thread = Thread(target=camera.launch_video)
    capture_Thread.start()

    # Initialisation du service de description d'environnement
    env_model = EnvironmentModel()

    # A partir de la on peut mettre la camera en pause ou en lecture
    camera.pause_video()
    currentContext = camera.get_context  # On peut recuperer le contexte courant qui est le nom du dossier ou la
    # camera enregistre actuellement les images
    currentIndex = camera.get_index  # Correspond a l'index de l'image de la derniere capture

    # On peut alors utiliser le service de description d'environnement pour la description de l'environnement L url
    # correspond a l url du serveur qui permet de télécharger l'image notamment celle du reverse proxy ngrok suivit
    # du currentContext / currentIndex +.png

    env_model.describe_environment("adresse du reverse proxy /" + currentContext + "/" +
                                   currentIndex + ".png")

    print(currentContext)
    print(currentIndex)
