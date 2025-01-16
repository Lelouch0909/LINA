from langchain.llms import BaseLLM
from langchain.schema import LLMResult, Generation
from pydantic import Field
from mistralai import Mistral
from typing import List
 
class MistralAPIWrapper(BaseLLM):
    api_key: str = Field(default="73SIFMtxPSQHBaqO2zFwv5AS44ewsKtc", description="La clé API pour accéder à Mistral.")
    client: Mistral = Field(default=None, description="Le client Mistral.")

    def __init__(self, api_key: str = "73SIFMtxPSQHBaqO2zFwv5AS44ewsKtc"):
        super().__init__(api_key=api_key)  # Initialiser la classe parente avec api_key
        self.client = Mistral(api_key=api_key)  # Initialiser le client Mistral

    def _generate(self, prompts: List[str], **kwargs) -> LLMResult:
        """Envoie une requête à l'API Mistral pour générer une réponse pour chaque prompt."""
        responses = []
        for prompt in prompts:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            # Encapsuler chaque réponse dans un objet Generation
            responses.append([Generation(text=response.choices[0].message.content)])
        return LLMResult(generations=responses)

    def _llm_type(self) -> str:
        """Retourne le type de LLM (utilisé par LangChain)."""
        return "mistral"