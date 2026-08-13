from models.sortie_model import SortieModel


class SortieController:

    def __init__(self):

        self.model = SortieModel()

    # =====================================================
    # AJOUTER UNE SORTIE
    # =====================================================

    def ajouter_sortie(

        self,
        product_id,
        quantite,
        client,
        numero_bon,
        commentaire

    ):

        # =================================================
        # Vérification quantité
        # =================================================

        try:

            quantite = int(quantite)

        except (ValueError, TypeError):

            raise Exception(
                "La quantité doit être un nombre entier."
            )

        # =================================================
        # Quantité positive
        # =================================================

        if quantite <= 0:

            raise Exception(
                "La quantité doit être supérieure à 0."
            )

        # =================================================
        # Vérifier produit
        # =================================================

        if product_id is None:

            raise Exception(
                "Veuillez sélectionner un produit."
            )

        # =================================================
        # Ajouter sortie
        # =================================================

        self.model.ajouter_sortie(

            product_id,
            quantite,
            client,
            numero_bon,
            commentaire

        )

    # =====================================================
    # AFFICHER
    # =====================================================

    def get_all_sorties(self):

        return self.model.get_all_sorties()

    # =====================================================
    # FERMER
    # =====================================================

    def close(self):

        if getattr(self, 'model', None) and hasattr(self.model, 'close'):

            try:
                self.model.close()
            except Exception:
                pass