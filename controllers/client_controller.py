from models.client_model import ClientModel


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

    # =====================================================
    # SUPPRIMER
    # =====================================================

    def supprimer_client(
        self,
        id_client
    ):

        self.model.supprimer_client(
            id_client
        )

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