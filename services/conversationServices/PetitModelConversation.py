from transformers import GPT2LMHeadModel, GPT2Tokenizer


class PetitModeleConversation:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Définir le token de remplissage (caractère spécial pour compléter les séquences)
        self.predefined_prompts = {
            "greeting": "Hello, how can I assist you today?",
            "acknowledgment": "I'm on it, please give me a moment...",
            "confirmation": "You said: '{demand}'. Is that correct? (Please reply with 'Yes' or 'No')",
            "closing": " {response} thanks for the listening"
        }

    def respond(self, user_input, prompt_type="confirmation", response=None):
        # Récupérer le prompt en fonction du type (un prompt est un texte qui sert de contexte ou d'instruction)
        prompt = self.predefined_prompts.get(prompt_type, "")
        
        # Formater le prompt avec les variables appropriées
        if prompt_type == "confirmation":
            return self.predefined_prompts["confirmation"].format(demand=user_input)
        elif prompt_type == "closing":
            if response is None:
                raise ValueError("Le paramètre 'response' est requis pour le type de prompt 'closing'.")
            return self.predefined_prompts["closing"].format(response=response)

        # Encoder le prompt et générer la réponse (conversion du texte en nombres pour le modèle)
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = inputs.ne(self.tokenizer.pad_token_id).float()  # Créer le masque d'attention (indique au modèle quelles parties du texte sont réelles vs remplissage)

        outputs = self.model.generate(
            inputs,
            attention_mask=attention_mask,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,  # Définir l'ID du token de fin de séquence
            no_repeat_ngram_size=2,  # Éviter les répétitions de phrases (ngram = groupe de n mots consécutifs)
            do_sample=True,  # Activer l'échantillonnage pour plus de diversité (plutôt que de toujours choisir le mot le plus probable)
            top_k=50,  # Limiter les choix aux 50 meilleurs tokens (mots ou parties de mots)
            top_p=0.95,  # Utiliser l'échantillonnage nucleus (ne garde que les tokens représentant 95% de la probabilité totale)
            temperature=0.8  # Contrôler la créativité (plus la valeur est haute, plus les réponses seront diverses mais potentiellement moins pertinentes)
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
