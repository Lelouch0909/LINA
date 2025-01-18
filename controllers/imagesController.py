import os

from flask import Flask, send_from_directory

app = Flask(__name__)

IMAGE_DIR = os.path.abspath("./ressources/videos")


@app.route("/images/<chemin>/<image>")
def get_image(chemin: str, image: str):
    image_path = os.path.join(IMAGE_DIR, chemin)
    print(image_path)
    try:
        if os.path.exists(image_path):
            return send_from_directory(image_path, image)
        else:
            return {"error": "Image non trouvée a l'adresse " + image_path}
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image : {e}")
        return {"error": "Failed to retrieve the image."}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
