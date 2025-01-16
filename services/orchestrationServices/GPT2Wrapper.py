from langchain.llms import BaseLLM
from langchain.schema import LLMResult, Generation
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from pydantic import Field
from typing import List, Optional
import torch

class GPT2Wrapper(BaseLLM):
    tokenizer: Optional[GPT2Tokenizer] = Field(default=None, exclude=True)  # Déclarer comme champ Pydantic
    model: Optional[GPT2LMHeadModel] = Field(default=None, exclude=True)    # Déclarer comme champ Pydantic

    def __init__(self, model_name="gpt2", **kwargs):
        super().__init__(**kwargs)  # Initialiser la classe parente
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)  # Initialiser le tokenizer
        self.model = GPT2LMHeadModel.from_pretrained(model_name)    # Initialiser le modèle

    def _generate(self, prompts: List[str], **kwargs) -> LLMResult:
        responses = []
        for prompt in prompts:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,  # Utiliser max_new_tokens au lieu de max_length
                num_return_sequences=1
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            responses.append([Generation(text=response)])
        return LLMResult(generations=responses)

    def _llm_type(self) -> str:
        return "gpt2"