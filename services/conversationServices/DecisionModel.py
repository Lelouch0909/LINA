from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import StructuredTool
from services.conversationServices.Tools     import Tools
from services.orchestrationServices.MistralAPIWrapper import MistralAPIWrapper
from services.orchestrationServices.GPT2Wrapper import GPT2Wrapper

class DecisionModel:
    def __init__(self):
        self.model = MistralAPIWrapper()
        #self.model = GPT2Wrapper()  # Utiliser GPT-2 au lieu de Mistral

        self.tools = Tools()

        # Définir les outils LangChain
        self.tool_decrire_piece = StructuredTool(
            name="describe_room",
            func=lambda _={}: self.tools.decrire_piece(),  # Accepter un dictionnaire d'arguments
            description="Describes the room the user is in.",
            args_schema=None
        )
        self.tool_localiser_objet = StructuredTool(
            name="locate_object",
            func=lambda x: self.tools.localiser_objet(x),
            description="Locates an object or person.",
            args_schema=None
        )
        self.tool_decrire_objet = StructuredTool(
            name="describe_object",
            func=lambda x: self.tools.decrire_objet(x),
            description="Describes an object or person.",
            args_schema=None
        )

        # Prompt pour décider quel outil appeler
        self.prompt_decision = PromptTemplate(
            input_variables=["request"],
            template="""Analyzes the following request and determines which tool is most appropriate:
                - describe_room : Describes the room where the user is located.
                - locate_object : Locates an object or person.
                - describe_object : Describes an object or person.

                Request : {request}

                Response (describe_room, locate_object, describe_object or None):"""
        )

    def analyser_demande(self, demande: str) -> str:
        """Analyse la demande et détermine intelligemment quel outil appeler."""
        # Utiliser Mistral pour décider quel outil exécuter
        chain_decision = LLMChain(llm=self.model, prompt=self.prompt_decision) # GPT2Wrapper au lieu de MistralAPIWrapper
        decision = chain_decision.run(request=demande).strip()

        # Exécuter l'outil approprié
        if "describe_room" in decision:
            return self.tool_decrire_piece.run({})  # Passer un dictionnaire vide
        elif "locate_object" in decision:
            objet = self.extraire_objet(demande)  # Extraire l'objet ou la personne
            return self.tool_localiser_objet.run(objet)
        elif "describe_object" in decision:
            objet = self.extraire_objet(demande)  # Extraire l'objet ou la personne
            return self.tool_decrire_objet.run(objet)
        else:
            return "I am not designed for this task."  # Réponse par défaut en anglais

    def extraire_objet(self, demande: str) -> str:
        """Extrait l'objet ou la personne de la demande."""
        # Utiliser Mistral pour extraire l'objet ou la personne
        prompt = f"Extract the object or person mentioned in the request: {demande}"
        response = self.model.generate([prompt])  # GPT2Wrapper au lieu de MistralAPIWrapper
        return response.generations[0][0].text.strip()

if __name__ == "__main__":
    api_key = "ZfulYxd6lx7LBTVPUvhSXsHurD05Qkkl"  #la clé API Mistral
    grand_modele = DecisionModel()

    demande = "Décris la pièce où je me trouve."
    reponse = grand_modele.analyser_demande(demande)
    print(reponse)

    demande = "Où se trouve la télécommande ?"
    reponse = grand_modele.analyser_demande(demande)
    print(reponse)

    demande = "Décris-moi le canapé."
    reponse = grand_modele.analyser_demande(demande)
    print(reponse)

    demande = "Quel temps fait-il dehors ?"
    reponse = grand_modele.analyser_demande(demande)
    print(reponse)