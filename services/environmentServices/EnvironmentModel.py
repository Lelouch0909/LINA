import os

from huggingface_hub import InferenceClient

from services.audioServices.syntheseVocalService import SyntheseVocalService, Langue



# Represente le model charge de la description generale d un environnement


class EnvironmentModel:
    def __init__(self):
        self.client = InferenceClient(api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"))
        self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct"  # Model to use

    # Il s agit d un template pour la generation d un message predefini. Par la suite il y aura plein de ces
    # templates pour chaque cas de description en fonction des besoins

    def describe_environment(self, image_url, content):
        print("-------------------------------------------------------------")
        print("url de l'image dans la fonction decrire environnement :" +image_url)
        print("-------------------------------------------------------------")
        # On genere le message
        messages = generate_message(image_url,content)
        # Utiliser un modèle supportant l'analyse d'image
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=0.8,
            top_p=0.8,
            stream=False # On ne veut pas que le model stream la reponse car on veut la reponse complete
        )
        return self._extract_response_text(response)
        # text = []
        # vocal = SyntheseVocalService(Langue.EN)

        # for chunk in response:
        #     content = chunk.choices[0].delta.content
        #     if content:
        #         text.extend(content.split())
        #         while len(text) > 20:
        #             batch = text[:20]
        #             vocal.syntheseVocal(" ".join(batch))
        #             print(" ".join(batch))
        #             text = text[20:]

    def describe_object(self, image_url, content):
        print("-------------------------------------------------------------")
        print("url de l'image dans la fonction decrire objet :" +image_url)
        print("-------------------------------------------------------------")
        messages = generate_message(image_url, content)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=0.7,
            top_p=0.5,
            stream=False
        )
        return self._extract_response_text(response)
    
    def locate_object(self, image_url, content):
        print("-------------------------------------------------------------")
        print("url de l'image dans la fonction localiser objet :" +image_url)
        print("-------------------------------------------------------------")
        messages = generate_message(image_url, content)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=2000,
            temperature=1,
            top_p=1,
            stream=False
        )
        return self._extract_response_text(response)
    
    def _extract_response_text(self, response):
        """Extrait le texte de la réponse du modèle."""
        if response.choices and len(response.choices) > 0:
            message = response.choices[0].message
            if hasattr(message, 'content'):
                response_text = message.content
                print("Réponse du modèle :", response_text)
                return response_text
            else:
                print("Le champ 'content' est manquant dans la réponse.")
                return None
        else:
            print("Aucune réponse valide trouvée.")
            return None


def generate_message(image_url, content):
    messages = [

        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content

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
