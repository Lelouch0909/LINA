import os

from huggingface_hub import InferenceClient

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"


# Represente le model charge de la description generale d un environnement


class EnvironmentModel:
    def __init__(self):
        self.client = InferenceClient(api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
        self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct"  # Model to use

    # Il s agit d un template pour la generation d un message predefini. Par la suite il y aura plein de ces
    # templates pour chaque cas de description en fonction des besoins

    def describe_environment(self, image_url):
        messages = _generate_message(image_url)
        # Utiliser un modèle supportant l'analyse d'image
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=5000,
            temperature=0.9,
            top_p=0.9,
            stream=True
        )

        text = []
        for chunk in response:
            # Ici on utilisera la fonctionnalite de synthese vocal plutot qu un print
            print(chunk.choices[0].delta.content, end="")


def _generate_message(image_url):
    messages = [

        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """ You are an AI assistant for a blind person. Based on the provided images, you will provide the following information: the room the person is in, the closest exit, the location of dangerous objects, the number of people in the room, their appearance, their facial expressions, and their position, as well as the position of dangerous objects. Then, you will provide a description of the environment from your perspective, as if you were the person filming. The entire response should be formatted in JSON.
                    with the following format and fields"
                     Exemple de reponse; 
                    {
                        "room": "name of the room",
                        "exit": "if there is an exit, the name of the closest exit else null",
                        "dangerousObjects": { "name": "the dangerous object", "position": "the position of the object" },
                        "people": "description of the people and theirs position ex: n people are present in the ***; they are 2 meters away from you., ...",
                        "peopleDescription": [
                            "person1": {
                                "height": "1.8m, tall, standing near the counter, slightly to your left.",
                                "expression": "neutral",
                                "direction": "facing the stove"
                            },
                            "person2": {
                                "height": "1.75m, middle-aged man, standing near the sink, slightly to your right.",
                                "expression": "smiling",
                                "direction": "looking out the window"
                            },
                          ...
                        ],
                        "environmentDescription": "the description of the environment ex :This is a bright kitchen with neutral-colored walls, granite countertops, and stainless steel appliances. 
                        There are lots of utensils and kitchen gadgets scattered about the countertops. The air is thick with the aroma of food.
                         There's the constant hum of appliances in the background, punctuated by the occasional sound of sizzling or someone stirring the mixture."
                    } """

                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }
    ]

    return messages
