from models.client_model import ClientModel
from database.database import Database


class ClientController:

    def __init__(self):

        self.model = ClientModel()

    # =====================================================
    # AJOUTER
    # =====================================================

    def ajouter_client(
        self,
        nom,
        telephone,
        adresse,
        email,
        ville
    ):

        self.model.ajouter_client(
            nom,
            telephone,
            adresse,
            email,
            ville
        )
        try:
            db = Database()
            desc = f"Client {nom} créé"
            db.ajouter_historique("SYSTEM", "CREATE", "Client", desc)
        except Exception:
            pass

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_all_clients(self):

        return self.model.get_all_clients()

    # =====================================================
    # MODIFIER
    # =====================================================

    def modifier_client(
        self,
        id_client,
        nom,
        telephone,
        adresse,
        email,
        ville
    ):

        self.model.modifier_client(
            id_client,
            nom,
            telephone,
            adresse,
            email,
            ville
        )
        try:
            db = Database()
            desc = f"Client {nom} modifié (id={id_client})"
            db.ajouter_historique("SYSTEM", "UPDATE", "Client", desc)
        except Exception:
            pass

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer_client(
        self,
        id_client
    ):
        # Attempt to capture client info before deletion
        try:
            client = next((c for c in self.get_all_clients() if c[0] == id_client), None)
            nom = client[1] if client else ''
        except Exception:
            nom = ''

        self.model.supprimer_client(
            id_client
        )

        try:
            db = Database()
            desc = f"Client {nom} supprimé (id={id_client})"
            db.ajouter_historique("SYSTEM", "DELETE", "Client", desc)
        except Exception:
            pass

    # =====================================================
    # RECHERCHER
    # =====================================================

    def rechercher_client(
        self,
        mot
    ):

        return self.model.rechercher_client(
            mot
        )

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        if getattr(self, 'model', None) and hasattr(self.model, 'close'):

            try:
                self.model.close()
            except Exception:
                pass