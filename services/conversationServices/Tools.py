import os
from services.cameraServices.CaptureService import Camera
from services.environmentServices.EnvironmentModel import EnvironmentModel


class Tools:
    @staticmethod
    def decrire_piece(_=None) -> str:
        content = """
                    You are an AI assistant helping a blind person understand their surroundings. Given an image, provide a detailed description of the environment in JSON format, including:

                    The name of the room.

                    The closest exit, if available; otherwise, null.

                    Any dangerous objects present, with their positions.

                    The number of people in the room, their appearance, facial expressions, and positions relative to the camera.

                    A narrative description of the environment from the camera's perspective.

                    Adhere to the structure provided in the example response, using consistent units for distances and clear positional descriptors."

                    Example Response:
                    {
                    "room": "kitchen",
                    "exit": "door near the stove",
                    "dangerousObjects": [
                        {
                        "name": "knife",
                        "position": "on the counter to your left"
                        }
                    ],
                    "people": "Two people are in the room; one is near the stove, the other is by the sink.",
                    "peopleDescription": [
                        {
                        "person1": {
                            "height": "1.8m, tall, standing near the stove, slightly to your left.",
                            "expression": "neutral",
                            "direction": "facing the stove"
                        },
                        "person2": {
                            "height": "1.75m, middle-aged man, standing near the sink, slightly to your right.",
                            "expression": "smiling",
                            "direction": "looking out the window"
                        }
                        }
                    ],
                    "environmentDescription": "This is a bright kitchen with neutral-colored walls, granite countertops, and stainless steel appliances. There are lots of utensils and kitchen gadgets scattered about the countertops. The air is thick with the aroma of food. There's the constant hum of appliances in the background, punctuated by the occasional sound of sizzling or someone stirring the mixture."
                    }
        """
        camera = Camera()
        camera.pause_video()
        context = camera.get_context
        index = camera.get_index
        ngrok_url = os.getenv("NGROK_URL")
        image_url = f"{ngrok_url}/images/{context}/{index}.png"
        print("------------ Dans la fonciton decrire_piece ---------------------")
        print(image_url)
        env_model = EnvironmentModel()
        response = env_model.describe_environment(image_url,content)
        print(response)

        print("------------ Dans la fonciton decrire_piece ---------------------")
        return response

    @staticmethod
    def localiser_objet(objet: str) -> str:
        content = """
        You are an AI assistant helping a blind person understand their surroundings by locating specific objects in images.
        Given an image and an object name, provide a detailed description of each instance of the object's position and attributes in JSON format.
        Include each object's position relative to the person or other objects, its attributes, its relation to other objects, and a sensory description of its position. 
        If the object is not present in the image, indicate its absence.
        Example Response:
                    {
            "objectName": "book",
            "objectsFound": [
                {
                "position": "on the table, to the left of the lamp",
                "attributes": {
                    "color": "blue",
                    "size": "medium",
                    "shape": "rectangular"
                },
                "relationToOtherObjects": "next to a cup of coffee",
                "distance": "about 2 meters away from you",
                "sensoryDescription": "A blue book resting on the table, near the lamp and a cup of coffee."
                },
                {
                "position": "on the shelf, third from the left",
                "attributes": {
                    "color": "red",
                    "size": "small",
                    "shape": "square"
                },
                "relationToOtherObjects": "next to a picture frame",
                "distance": "about 3 meters away from you",
                "sensoryDescription": "A red book on the shelf, near a picture frame."
                }
            ]
}
 The object is : """ + objet + """
        """
        camera = Camera()
        camera.pause_video()
        context = camera.get_context
        index = camera.get_index
        ngrok_url = os.getenv("NGROK_URL")
        image_url = f"{ngrok_url}/images/{context}/{index}.png"
        print("------------ Dans la fonciton localiser_objet ---------------------")
        print(image_url)
        env_model = EnvironmentModel()
        response = env_model.locate_object(image_url,content)
        print(response)
        print("------------ Dans la fonciton localiser_objet ---------------------")
        return response
    
    
    @staticmethod
    def decrire_objet(objet: str) -> str:
      
        content = """        Describe """ + objet + """ in the provided image. Your response should be in JSON format, including the object's name, location, attributes, features, relation to other objects, and a sensory description. If the object is not found, indicate its absence. Follow the structure of the example response.
        Example Response:
        {
            "objectName": "cup",
            "location": "on the table, to the left of the plate",
            "attributes": {
                "color": "white",
                "size": "small",
                "shape": "cylindrical"
            },
            "features": "has a handle on the side, no designs",
            "relationToEnvironment": "next to a plate and a fork",
            "potentialUse": "for drinking",
            "sensoryDescription": "A small white cup with a handle, sitting on the table, ready to be used for drinking."
            }
        """
        camera = Camera()
        camera.pause_video()
        context = camera.get_context
        index = camera.get_index
        ngrok_url = os.getenv("NGROK_URL")
        image_url = f"{ngrok_url}/images/{context}/{index}.png"
        print("------------ Dans la fonciton decrire_objet ---------------------")
        print(image_url)
        env_model = EnvironmentModel()
        response = env_model.describe_object(image_url,content)
        print(response)
        print("------------ Dans la fonciton decrire_objet ---------------------")
        return response