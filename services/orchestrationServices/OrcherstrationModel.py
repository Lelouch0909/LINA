from services.audioServices.syntheseVocalService import Langue, SyntheseVocalService
from services.cameraServices.CaptureService import Camera
from services.conversationServices.PetitModelConversation import PetitModeleConversation
from services.conversationServices.DecisionModel import DecisionModel
from services.reconnaissanceVocale.ReconnaissanceVocalModel import ReconnaissanceVocalModel
import threading

class OrchestrationModel:
    def __init__(self,camera: Camera, langue: Langue = Langue.EN,  ):
        self.reconnaissance_vocale = ReconnaissanceVocalModel(keywords=["nina","lyna","lina","luna","nyna"])
        self.petit_modele = PetitModeleConversation()
        self.synthese_vocale = SyntheseVocalService(langue)
        self.grand_modele = DecisionModel() 
        self.camera = camera

    def lancer_conversation(self):
        """Lance le processus d'orchestration."""
        self.synthese_vocale.syntheseVocal("Starting conversation. Waiting for the keyword 'nina'...")
        self.reconnaissance_vocale.commencer_l_ecoute()

        while True:
            # Étape 1 : Récupérer et confirmer la demande
            demande_confirmee = self.recuperer_et_confirmer_demande()
            if not demande_confirmee:
                continue  # Si la demande n'est pas confirmée, recommencer
            self.camera.pause_video()

            # Étape 2 : Traiter la demande avec le grand modèle
            reponse_finale = self.traiter_demande(demande_confirmee)

            # Étape 3 : Générer la réponse finale
            self.synthese_vocale.syntheseVocal(reponse_finale)
            self.synthese_vocale.syntheseVocal("Conversation ended. Waiting for a new request...")
            self.camera.resume_video()
            
    def recuperer_et_confirmer_demande(self):
        """Récupère la demande vocale et la confirme avec l'utilisateur."""
        # Étape 1 : Récupérer la demande vocale
        demande = self.reconnaissance_vocale.ecouter_et_enregistrer()
        if not demande:
            self.synthese_vocale.syntheseVocal("No request detected. Waiting...")
            return None

        # Étape 2 : Confirmer la demande avec le petit modèle
        confirmation = self.petit_modele.respond(demande, prompt_type="confirmation")
        self.synthese_vocale.syntheseVocal(confirmation)  # Synthèse vocale de la confirmation

        # Étape 3 : Récupérer la réponse de l'utilisateur
        reponse_utilisateur = self.reconnaissance_vocale.ecouter_et_enregistrer()
        if "yes" in reponse_utilisateur.lower():
            self.synthese_vocale.syntheseVocal("Request confirmed.")
            return demande
        else:
            self.synthese_vocale.syntheseVocal("Request not confirmed. Restarting...")
            return None

    def traiter_demande(self, demande):
            """Traite la demande avec le grand modèle et retourne la réponse finale."""
            
            # Étape 1 : Afficher un message d'accusé de réception
            acknowledgment = self.petit_modele.respond(demande, prompt_type="acknowledgment")
            
            # Fonction pour gérer la synthèse vocale avec gestion des erreurs
            def synthese_vocale_safe(text):
                try:
                    self.synthese_vocale.syntheseVocal(text)
                except Exception as e:
                    print(f"Erreur lors de la synthèse vocale : {e}")

            # Lancer la synthèse vocale dans un thread séparé
            acknowledgment_thread = threading.Thread(
                target=synthese_vocale_safe,
                args=(acknowledgment,)
            )
            acknowledgment_thread.start()

            try:
                # Étape 2 : Traiter la demande avec le grand modèle
                reponse_grand_modele = self.grand_modele.analyser_demande(demande)  # À implémenter
            except Exception as e:
                print(f"Erreur lors de l'analyse de la demande avec le grand modèle : {e}")
                return "Sorry, I couldn't process your request."

            # Étape 3 : Générer la réponse finale avec le petit modèle
            reponse_finale = self.petit_modele.respond(reponse_grand_modele, prompt_type="closing", response=reponse_grand_modele)
            return reponse_finale
